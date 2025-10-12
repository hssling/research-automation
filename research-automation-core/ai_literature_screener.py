"""
AI-Assisted Literature Screening System
Uses machine learning and NLP to assist with literature screening in systematic reviews
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from typing import List, Dict, Any, Tuple, Optional
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import logging
import pickle
import os
from pathlib import Path

# NLP setup
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AILiteratureScreener:
    """
    AI-powered literature screening assistant for systematic reviews
    """

    def __init__(self, model_path: str = None):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2
        )
        self.models = {}
        self.model_path = Path(model_path) if model_path else Path("research-automation-core/models")

        if model_path and self.model_path.exists():
            self.load_models()

        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for ML analysis"""
        if not text or pd.isna(text):
            return ""

        # Convert to lowercase
        text = str(text).lower()

        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stop words and stem
        tokens = [self.stemmer.stem(word) for word in tokens
                 if word not in self.stop_words and len(word) > 2]

        return ' '.join(tokens)

    def prepare_training_data(self, csv_file: str,
                            text_column: str,
                            label_column: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare training data from labeled literature

        Args:
            csv_file: Path to CSV file with labeled data
            text_column: Name of column containing text
            label_column: Name of column containing labels (include/exclude)

        Returns:
            Tuple of (X_features, y_labels)
        """
        logger.info(f"Loading training data from {csv_file}")

        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} training samples")

        # Filter out unlabeled data
        df = df.dropna(subset=[text_column, label_column])
        logger.info(f"Kept {len(df)} labeled samples")

        # Convert labels to binary
        df[label_column] = df[label_column].str.lower()
        df[label_column] = df[label_column].map({
            'include': 1, 'included': 1, 'yes': 1, 'y': 1,
            'exclude': 0, 'excluded': 0, 'no': 0, 'n': 0
        })

        # Remove ambiguous labels
        df = df.dropna(subset=[label_column])
        df[label_column] = df[label_column].astype(int)

        logger.info(f"Final training samples: {len(df)}")
        logger.info(f"Class distribution: {df[label_column].value_counts().to_dict()}")

        # Preprocess text
        logger.info("Preprocessing text data...")
        df['processed_text'] = df[text_column].apply(self.preprocess_text)

        # Vectorize text
        logger.info("Vectorizing text data...")
        X = self.vectorizer.fit_transform(df['processed_text'])
        y = df[label_column].values

        return X, y

    def train_model(self, X: np.ndarray, y: np.ndarray,
                   model_type: str = 'logistic') -> Any:
        """
        Train a classification model

        Args:
            X: Feature matrix
            y: Target labels
            model_type: Type of model ('logistic', 'svm', 'naive_bayes')

        Returns:
            Trained model
        """
        logger.info(f"Training {model_type} model...")

        if model_type == 'logistic':
            model = LogisticRegression(random_state=42, max_iter=1000)
        elif model_type == 'svm':
            model = SVC(kernel='linear', random_state=42, probability=True)
        elif model_type == 'naive_bayes':
            model = MultinomialNB()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        # Cross-validation for model selection
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1')
        logger.info(".3f")

        # Train final model
        model.fit(X, y)

        # Save model
        model_name = f"{model_type}_screening_model"
        self.models[model_name] = model

        return model

    def train_ensemble(self, X: np.ndarray, y: np.ndarray) -> Any:
        """Train an ensemble of different models"""
        logger.info("Training ensemble model...")

        models = []
        model_types = ['logistic', 'naive_bayes', 'svm']

        for model_type in model_types:
            logger.info(f"Training {model_type} model...")
            if model_type == 'logistic':
                model = LogisticRegression(random_state=42, max_iter=1000)
            elif model_type == 'svm':
                model = SVC(kernel='linear', random_state=42, probability=True)
            elif model_type == 'naive_bayes':
                model = MultinomialNB()

            model.fit(X, y)
            models.append((model_type, model))

        self.models['ensemble'] = models
        logger.info("Ensemble model trained")

        return models

    def predict_screening_decision(self, text: str, model_name: str = 'logistic_screening_model') -> Dict[str, Any]:
        """
        Predict screening decision for a single text

        Args:
            text: Text to classify
            model_name: Name of model to use

        Returns:
            Dictionary with prediction results
        """
        processed_text = self.preprocess_text(text)

        if processed_text.strip() == "":
            return {
                'decision': 'unclear',
                'confidence': 0.0,
                'probabilities': {'exclude': 0.5, 'include': 0.5}
            }

        # Vectorize text
        X = self.vectorizer.transform([processed_text])

        if model_name == 'ensemble' and 'ensemble' in self.models:
            # Use ensemble prediction
            predictions = []
            probabilities = []

            for model_type, model in self.models['ensemble']:
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(X)[0]
                    probabilities.append(proba)
                else:
                    pred = model.predict(X)[0]
                    predictions.append(pred)

            if probabilities:
                avg_proba = np.mean(probabilities, axis=0)
                decision = 'include' if avg_proba[1] > 0.5 else 'exclude'
                confidence = max(avg_proba[1], avg_proba[0])
            else:
                avg_pred = np.mean(predictions)
                decision = 'include' if avg_pred > 0.5 else 'exclude'
                confidence = abs(avg_pred - 0.5) * 2

            return {
                'decision': decision,
                'confidence': confidence,
                'probabilities': {'exclude': 1-confidence, 'include': confidence}
            }

        elif model_name in self.models:
            model = self.models[model_name]

            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(X)[0]
                decision = 'include' if probabilities[1] > probabilities[0] else 'exclude'
                confidence = max(probabilities[1], probabilities[0])
            else:
                prediction = model.predict(X)[0]
                decision = 'include' if prediction == 1 else 'exclude'
                confidence = 0.8 if abs(prediction - 0.5) > 0.3 else 0.5

            return {
                'decision': decision,
                'confidence': confidence,
                'probabilities': {'exclude': 1-confidence, 'include': confidence}
            }

        else:
            logger.warning(f"Model {model_name} not found. Using random prediction.")
            return {
                'decision': 'review_required',
                'confidence': 0.0,
                'probabilities': {'exclude': 0.5, 'include': 0.5}
            }

    def screen_literature(self, csv_file: str,
                         text_column: str,
                         output_file: str = None,
                         model_name: str = 'logistic_screening_model',
                         confidence_threshold: float = 0.7) -> pd.DataFrame:
        """
        Screen literature using the trained AI model

        Args:
            csv_file: Path to CSV file with literature to screen
            text_column: Name of column containing text to screen
            output_file: Path to save results (optional)
            model_name: Name of model to use for screening
            confidence_threshold: Minimum confidence for automatic decision

        Returns:
            DataFrame with screening results
        """

        logger.info(f"Loading literature from {csv_file}")
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} records for screening")

        # Apply AI screening
        results = []
        for idx, row in df.iterrows():
            text = row[text_column] if pd.notna(row[text_column]) else ""

            prediction = self.predict_screening_decision(text, model_name)

            result = {
                'original_text': text,
                'processed_text': self.preprocess_text(text),
                'ai_decision': prediction['decision'],
                'ai_confidence': prediction['confidence'],
                'probability_include': prediction['probabilities']['include'],
                'probability_exclude': prediction['probabilities']['exclude'],
                'needs_review': prediction['confidence'] < confidence_threshold,
                'final_decision': None,  # To be filled by human reviewer
                'reviewer_notes': ''
            }

            # Add original columns
            result.update(row.to_dict())
            results.append(result)

            if (idx + 1) % 100 == 0:
                logger.info(f"Processed {idx + 1}/{len(df)} records")

        screened_df = pd.DataFrame(results)

        # Calculate summary statistics
        summary = screened_df['ai_decision'].value_counts().to_dict()
        confidence_stats = screened_df['ai_confidence'].describe()
        needs_review_count = screened_df['needs_review'].sum()

        logger.info("Screening Summary:")
        logger.info(f"Records processed: {len(screened_df)}")
        logger.info(f"AI decisions: {summary}")
        logger.info(".2f")
        logger.info(f"Records needing manual review: {needs_review_count}")

        # Save results if requested
        if output_file:
            screened_df.to_csv(output_file, index=False)
            logger.info(f"Results saved to {output_file}")

        return screened_df

    def save_models(self, models_dir: str = None):
        """Save trained models to disk"""
        if not models_dir:
            models_dir = self.model_path
        else:
            models_dir = Path(models_dir)

        models_dir.mkdir(parents=True, exist_ok=True)

        # Save vectorizer
        vectorizer_path = models_dir / "vectorizer.pkl"
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)

        # Save models
        for model_name, model in self.models.items():
            model_path = models_dir / f"{model_name}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

        logger.info(f"Models saved to {models_dir}")

    def load_models(self, models_dir: str = None):
        """Load trained models from disk"""
        if not models_dir:
            models_dir = self.model_path
        else:
            models_dir = Path(models_dir)

        if not models_dir.exists():
            logger.warning(f"Models directory {models_dir} does not exist")
            return

        # Load vectorizer
        vectorizer_path = models_dir / "vectorizer.pkl"
        if vectorizer_path.exists():
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)

        # Load models
        for model_file in models_dir.glob("*.pkl"):
            if model_file.name != "vectorizer.pkl":
                model_name = model_file.stem
                with open(model_file, 'rb') as f:
                    self.models[model_name] = pickle.load(f)

        logger.info(f"Loaded {len(self.models)} models from {models_dir}")

    def evaluate_model(self, X: np.ndarray, y: np.ndarray,
                       model_name: str = None) -> Dict[str, Any]:
        """
        Evaluate model performance

        Args:
            X: Feature matrix
            y: True labels
            model_name: Name of model to evaluate

        Returns:
            Dictionary with evaluation metrics
        """

        if not model_name or model_name not in self.models:
            model_name = list(self.models.keys())[0] if self.models else None
            if not model_name:
                raise ValueError("No models available for evaluation")

        model = self.models[model_name]

        # Split data for evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        report = classification_report(y_test, y_pred, output_dict=True)

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        evaluation_results = {
            'accuracy': report['accuracy'],
            'precision_include': report['1.0']['precision'],
            'recall_include': report['1.0']['recall'],
            'f1_include': report['1.0']['f1-score'],
            'precision_exclude': report['0.0']['precision'],
            'recall_exclude': report['0.0']['recall'],
            'f1_exclude': report['0.0']['f1-score'],
            'confusion_matrix': cm.tolist(),
            'classification_report': report
        }

        logger.info("Model Evaluation Results:")
        logger.info(".3f")
        logger.info(f"Include Precision: {evaluation_results['precision_include']:.3f}")
        logger.info(f"Include Recall: {evaluation_results['recall_include']:.3f}")
        logger.info(f"Include F1: {evaluation_results['f1_include']:.3f}")

        return evaluation_results

    def get_model_statistics(self) -> Dict[str, Any]:
        """Get statistics about available models"""
        stats = {
            'num_models': len(self.models),
            'model_names': list(self.models.keys()),
            'vectorizer_features': len(self.vectorizer.vocabulary_) if hasattr(self.vectorizer, 'vocabulary_') else 0
        }

        return stats


def train_ai_screener(training_data_path: str,
                     text_column: str = 'title_abstract',
                     label_column: str = 'decision',
                     output_dir: str = "models") -> Tuple[AILiteratureScreener, Dict[str, Any]]:
    """
    Convenience function to train an AI literature screener

    Args:
        training_data_path: Path to labeled training data CSV
        text_column: Name of column containing text data
        label_column: Name of column containing labels
        output_dir: Directory to save trained models

    Returns:
        Trained screener and evaluation results
    """

    logger.info("Training AI Literature Screener")
    logger.info("=" * 50)

    # Initialize screener
    screener = AILiteratureScreener()

    # Prepare training data
    X, y = screener.prepare_training_data(
        training_data_path, text_column, label_column
    )

    # Train models
    logger.info("Training individual models...")
    lr_model = screener.train_model(X, y, 'logistic')
    nb_model = screener.train_model(X, y, 'naive_bayes')
    svm_model = screener.train_model(X, y, 'svm')

    logger.info("Training ensemble model...")
    ensemble = screener.train_ensemble(X, y)

    # Evaluate models
    logger.info("Evaluating models...")
    lr_eval = screener.evaluate_model(X, y, 'logistic_screening_model')
    nb_eval = screener.evaluate_model(X, y, 'naive_bayes_screening_model')
    svm_eval = screener.evaluate_model(X, y, 'svm_screening_model')

    # Save models
    screener.save_models(output_dir)

    # Prepare evaluation summary
    evaluation_results = {
        'logistic_regression': lr_eval,
        'naive_bayes': nb_eval,
        'svm': svm_eval,
        'best_model': max([
            ('logistic', lr_eval['f1_include']),
            ('naive_bayes', nb_eval['f1_include']),
            ('svm', svm_eval['f1_include'])
        ], key=lambda x: x[1])[0]
    }

    logger.info("Training completed successfully!")
    logger.info(f"Models saved to: {output_dir}")
    logger.info(f"Recommended model: {evaluation_results['best_model']}")

    return screener, evaluation_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Literature Screener")
    parser.add_argument("action", choices=["train", "screen", "evaluate"],
                       help="Action to perform")
    parser.add_argument("--training-data", help="Path to training data CSV")
    parser.add_argument("--text-column", default="title_abstract",
                       help="Name of text column")
    parser.add_argument("--label-column", default="decision",
                       help="Name of label column")
    parser.add_argument("--screen-data", help="Path to data to screen")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--model", default="logistic_screening_model",
                       help="Model to use for screening")
    parser.add_argument("--models-dir", default="models",
                       help="Directory containing trained models")

    args = parser.parse_args()

    screener = AILiteratureScreener(args.models_dir)

    if args.action == "train":
        if not args.training_data:
            parser.error("--training-data required for training")

        screener, results = train_ai_screener(
            args.training_data,
            args.text_column,
            args.label_column,
            args.models_dir
        )

        print("Training Results:")
        print(f"Best Model: {results['best_model']}")

    elif args.action == "screen":
        if not args.screen_data:
            parser.error("--screen-data required for screening")

        screened_df = screener.screen_literature(
            args.screen_data,
            args.text_column,
            args.output,
            args.model
        )

        print(f"Screening completed. Results saved to {args.output}")

    elif args.action == "evaluate":
        if not args.training_data:
            parser.error("--training-data required for evaluation")

        X, y = screener.prepare_training_data(
            args.training_data,
            args.text_column,
            args.label_column
        )

        eval_results = screener.evaluate_model(X, y, args.model)

        print("Model Evaluation:")
        print(f"Accuracy: {eval_results['accuracy']:.3f}")
        print(f"F1 Score (Include): {eval_results['f1_include']:.3f}")
