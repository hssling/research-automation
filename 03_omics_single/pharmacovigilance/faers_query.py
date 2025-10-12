#!/usr/bin/env python3
"""
FAERS Database Query Tool for Pharmacovigilance Analysis
Automated adverse event data retrieval and analysis from FDA FAERS database
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging
from datetime import datetime
import argparse

class FAERSQuery:
    """
    Query FDA Adverse Event Reporting System (FAERS) database
    """

    def __init__(self, config):
        """
        Initialize FAERS database connection

        Args:
            config (dict): Database configuration parameters
        """
        self.config = config
        self.connection = None
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename='../results/pharmacovigilance/faers_analysis.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                logging.info("Successfully connected to FAERS database")
                print("🔗 Connected to FAERS database")
        except Error as e:
            logging.error(f"Error connecting to FAERS database: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Disconnected from FAERS database")

    def get_adverse_events_by_drug(self, drug_name, limit=1000):
        """
        Retrieve adverse events for a specific drug

        Args:
            drug_name (str): Name of the drug to query
            limit (int): Maximum number of records to return

        Returns:
            pd.DataFrame: Adverse event data
        """
        query = """
        SELECT
            faers.primaryid,
            faers.caseid,
            faers.drug_seq,
            faers.role_cod,
            faers.drugname,
            faers.val_vbm,
            faers.route,
            faers.dose_amt,
            faers.dose_unit,
            faers.dose_form,
            faers.dose_freq,
            faers.lot_num,
            faers.exp_dt,
            faers.rept_date,
            faers.age,
            faers.age_cod,
            faers.pt,
            faers.outcome_cod
        FROM DEMO_FAERS faers
        WHERE drugname LIKE %s
        AND rept_date >= 20100101
        AND rept_date <= 20231231
        ORDER BY rept_date DESC
        LIMIT %s
        """

        try:
            df = pd.read_sql_query(query, self.connection, params=(f'%{drug_name}%', limit))
            logging.info(f"Retrieved {len(df)} adverse events for {drug_name}")
            return df
        except Error as e:
            logging.error(f"Error querying adverse events: {e}")
            raise

    def get_adverse_events_by_event(self, event_term, limit=1000):
        """
        Retrieve records by adverse event term

        Args:
            event_term (str): Adverse event preferred term
            limit (int): Maximum number of records to return

        Returns:
            pd.DataFrame: Adverse event data
        """
        query = """
        SELECT
            faers.primaryid,
            faers.caseid,
            faers.drugname,
            faers.pt,
            faers.outcome_cod,
            faers.age,
            faers.sex,
            faers.rept_date,
            faers.fda_dt
        FROM DEMO_FAERS faers
        WHERE pt LIKE %s
        AND rept_date >= 20100101
        AND rept_date <= 20231231
        ORDER BY rept_date DESC
        LIMIT %s
        """

        try:
            df = pd.read_sql_query(query, self.connection, params=(f'%{event_term}%', limit))
            logging.info(f"Retrieved {len(df)} adverse events for {event_term}")
            return df
        except Error as e:
            logging.error(f"Error querying adverse events: {e}")
            raise

    def calculate_reporting_rates(self, df, drug_name=None):
        """
        Calculate adverse event reporting rates and frequencies

        Args:
            df (pd.DataFrame): Adverse event data
            drug_name (str): Specific drug name for filtering (optional)

        Returns:
            pd.DataFrame: Summary statistics
        """
        if drug_name:
            df = df[df['drugname'].str.contains(drug_name, case=False, na=False)]

        # Group by adverse event and drug
        summary = df.groupby(['pt', 'drugname']).size().reset_index(name='count')

        # Sort by frequency
        summary = summary.sort_values('count', ascending=False)

        # Calculate percentages
        total_events = len(df)
        summary['percentage'] = (summary['count'] / total_events * 100).round(2)

        logging.info(f"Calculated summary statistics for {len(summary)} adverse event types")

        return summary

    def analyze_signal_detection(self, df, minimum_reports=3):
        """
        Basic signal detection analysis using proportional reporting ratios (PRR)

        Args:
            df (pd.DataFrame): Adverse event data
            minimum_reports (int): Minimum number of reports for signal consideration

        Returns:
            pd.DataFrame: Signal detection results
        """
        # This is a simplified version - in practice, signal detection would
        # involve comparing against background rates from the entire database

        # Count adverse events by drug-event combination
        signal_df = df.groupby(['drugname', 'pt']).size().reset_index(name='count')

        # Filter for minimum reporting threshold
        signal_df = signal_df[signal_df['count'] >= minimum_reports]

        # Calculate basic statistics (simplified PRR approximation)
        total_by_drug = signal_df.groupby('drugname')['count'].sum()
        total_by_event = signal_df.groupby('pt')['count'].sum()

        signal_df['drug_total'] = signal_df['drugname'].map(total_by_drug)
        signal_df['event_total'] = signal_df['pt'].map(total_by_event)

        # Calculate expected count
        total_reports = signal_df['count'].sum()
        signal_df['expected'] = (signal_df['drug_total'] * signal_df['event_total']) / total_reports

        # Calculate PRR
        signal_df['prr'] = signal_df['count'] / signal_df['expected']

        # Sort by PRR descending
        signal_df = signal_df.sort_values('prr', ascending=False)

        logging.info(f"Analyzed {len(signal_df)} potential safety signals")

        return signal_df

def main():
    """Main function for FAERS analysis"""
    parser = argparse.ArgumentParser(description='FAERS Database Query Tool')
    parser.add_argument('--drug', type=str, help='Drug name to analyze')
    parser.add_argument('--event', type=str, help='Adverse event term to analyze')
    parser.add_argument('--limit', type=int, default=1000, help='Maximum records to retrieve')
    parser.add_argument('--output', type=str, default='../results/pharmacovigilance', help='Output directory')

    args = parser.parse_args()

    # Database configuration (example - replace with actual credentials)
    db_config = {
        'host': 'faers-db-host',
        'database': 'faers',
        'user': 'faers_user',
        'password': 'faers_password'
    }

    # Initialize FAERS query
    faers = FAERSQuery(db_config)

    try:
        # Connect to database
        faers.connect()

        if args.drug:
            print(f"🔍 Querying adverse events for drug: {args.drug}")
            df = faers.get_adverse_events_by_drug(args.drug, args.limit)

            print(f"📊 Retrieved {len(df)} records")

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{args.output}/{args.drug}_adverse_events_{timestamp}.csv"
            df.to_csv(output_file, index=False)

            # Generate summary
            summary = faers.calculate_reporting_rates(df, args.drug)
            summary_file = f"{args.output}/{args.drug}_summary_{timestamp}.csv"
            summary.to_csv(summary_file, index=False)

            # Signal detection
            signals = faers.analyze_signal_detection(df)
            signal_file = f"{args.output}/{args.drug}_signals_{timestamp}.csv"
            signals.to_csv(signal_file, index=False)

            print(f"💾 Results saved to {args.output}")

        elif args.event:
            print(f"🔍 Querying records for adverse event: {args.event}")
            df = faers.get_adverse_events_by_event(args.event, args.limit)

            print(f"📊 Retrieved {len(df)} records")

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{args.output}/{args.event}_events_{timestamp}.csv"
            df.to_csv(output_file, index=False)

            print(f"💾 Results saved to {args.output}")

        else:
            print("❌ Please specify either --drug or --event parameter")

    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"❌ Error: {e}")

    finally:
        faers.disconnect()

if __name__ == '__main__':
    main()
