# 🚀 Research Automation Platform - Laravel API Setup Guide

## 📋 Prerequisites Checklist

### ✅ MySQL Installation (Required First)
- [ ] MySQL Server installed and running
- [ ] Database user with create/drop privileges
- [ ] `mysql` command available in PATH

### ✅ PHP Environment
- [ ] PHP 8.1+ installed with extensions:
  - php-mysql
  - php-json
  - php-curl
  - php-zip
  - php-mbstring
  - php-xml
  - php-intl

### ✅ Composer Package Manager
- [ ] Composer installed globally
- [ ] Command: `composer --version`

---

## 🏗️ Step-by-Step Laravel Installation

### 1. Create Laravel Project
```bash
# Navigate to your project directory
cd d:\research-automation

# Create Laravel project
composer create-project laravel/laravel research-automation-api
cd research-automation-api
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with database credentials
nano .env  # or use VS Code

# Database configuration
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=research_automation_production
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
```

### 3. Generate Application Key
```bash
php artisan key:generate
```

### 4. Test Database Connection
```bash
php artisan migrate:status
# Should show "No migrations found" if connection successful
```

---

## 📊 Generate Eloquent Models & Migrations

### Core Models (Execute in order):
```bash
# User Management
php artisan make:model User -m
php artisan make:model UserExpertise -m

# Research Projects
php artisan make:model ResearchProject -m
php artisan make:model ProjectCollaborator -m

# Literature Management
php artisan make:model LiteratureArticle -m
php artisan make:model LiteratureSearch -m
php artisan make:model SearchResult -m

# Data Extraction & Quality
php artisan make:model ExtractionForm -m
php artisan make:model ExtractedData -m
php artisan make:model QualityAssessment -m

# Meta-Analysis
php artisan make:model MetaAnalysis -m
php artisan make:model MetaAnalysisResult -m

# Manuscripts
php artisan make:model Manuscript -m
php artisan make:model ManuscriptVersion -m

# Security
php artisan make:model ApiToken -m

# Logging
php artisan make:model SystemLog -m
```

---

## 🔗 Update Model Relationships

### Update `app/Models/User.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    protected $fillable = [
        'email', 'password', 'full_name', 'institution', 'research_field', 'role', 'api_key',
        'email_verified', 'two_factor_enabled', 'account_status', 'profile_picture_url',
        'bio', 'orcid_id'
    ];

    protected $hidden = ['password', 'remember_token'];
    protected $casts = ['email_verified_at' => 'datetime'];

    // Relationships
    public function projectsOwned() { return $this->hasMany(ResearchProject::class, 'owner_id'); }
    public function projectCollaborations() { return $this->belongsToMany(ResearchProject::class, 'project_collaborators'); }
    public function userExpertise() { return $this->hasMany(UserExpertise::class); }
    public function extractions() { return $this->hasMany(ExtractedData::class, 'extracted_by'); }
    public function qualityAssessments() { return $this->hasMany(QualityAssessment::class, 'assessed_by'); }
    public function manuscripts() { return $this->hasMany(Manuscript::class, 'created_by'); }
    public function manuscriptVersions() { return $this->hasMany(ManuscriptVersion::class, 'created_by'); }
    public function apiTokens() { return $this->hasMany(ApiToken::class); }
    public function systemLogs() { return $this->hasMany(SystemLog::class); }
}
```

### Update `app/Models/ResearchProject.php`
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ResearchProject extends Model
{
    use HasFactory;

    protected $fillable = [
        'title', 'description', 'research_question', 'methodology', 'status',
        'owner_id', 'funding_source', 'grant_number', 'clinical_trial_number',
        'target_population', 'intervention', 'comparator', 'outcome_measures',
        'prisma_registered', 'prospero_registration_number',
        'start_date', 'target_completion_date', 'actual_completion_date',
        'visibility', 'repository_url', 'preprint_url', 'keywords', 'research_tags'
    ];

    protected $casts = [
        'keywords' => 'json',
        'research_tags' => 'json',
        'prisma_registered' => 'boolean',
        'start_date' => 'date',
        'target_completion_date' => 'date',
        'actual_completion_date' => 'date'
    ];

    // Relationships
    public function owner() { return $this->belongsTo(User::class, 'owner_id'); }
    public function collaborators() { return $this->belongsToMany(User::class, 'project_collaborators'); }
    public function literatureSearches() { return $this->hasMany(LiteratureSearch::class); }
    public function extractedData() { return $this->hasMany(ExtractedData::class); }
    public function metaAnalyses() { return $this->hasMany(MetaAnalysis::class); }
    public function manuscripts() { return $this->hasMany(Manuscript::class); }
    public function qualityAssessments() { return $this->hasMany(QualityAssessment::class); }
}
```

---

## 🌐 Create API Routes

### Update `routes/api.php`
```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\{
    ResearchProjectController,
    LiteratureSearchController,
    DataExtractionController,
    MetaAnalysisController,
    ManuscriptController,
    UserController
};

// Research Project Management
Route::apiResource('research-projects', ResearchProjectController::class);

// Literature Management
Route::prefix('literature')->group(function () {
    Route::post('searches', [LiteratureSearchController::class, 'execute']);
    Route::get('searches/{id}/results', [LiteratureSearchController::class, 'results']);
    Route::put('articles/{id}/screening', [LiteratureSearchController::class, 'updateScreening']);
});

// Data Extraction & Quality Assessment
Route::prefix('extraction')->group(function () {
    Route::get('forms', [DataExtractionController::class, 'getForms']);
    Route::post('forms', [DataExtractionController::class, 'createForm']);
    Route::post('data', [DataExtractionController::class, 'saveExtraction']);
    Route::post('quality-assessment', [DataExtractionController::class, 'assessQuality']);
});

// Meta-Analysis Engine
Route::prefix('meta-analysis')->group(function () {
    Route::post('{projectId}/execute', [MetaAnalysisController::class, 'execute']);
    Route::get('{analysisId}/results', [MetaAnalysisController::class, 'getResults']);
    Route::post('{analysisId}/export', [MetaAnalysisController::class, 'exportResults']);
});

// Manuscript Generation
Route::prefix('manuscripts')->group(function () {
    Route::post('generate-with-ai', [ManuscriptController::class, 'generateWithAI']);
    Route::post('{manuscriptId}/versions', [ManuscriptController::class, 'createVersion']);
    Route::post('{manuscriptId}/export', [ManuscriptController::class, 'exportToWord']);
});

// User Management & Collaboration
Route::prefix('users')->group(function () {
    Route::get('projects', [UserController::class, 'getProjects']);
    Route::post('projects/{projectId}/collaborators', [UserController::class, 'inviteCollaborator']);
    Route::get('notifications', [UserController::class, 'getNotifications']);
});

// Protected routes (require authentication)
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', function (Request $request) {
        return $request->user();
    });

    Route::post('/tokens/create', function (Request $request) {
        $token = $request->user()->createToken($request->name);
        return ['token' => $token->plainTextToken];
    });
});
```

---

## 🔧 Next Steps After Setup

### 1. Test Basic API Endpoints
```bash
php artisan route:list
# Should show all registered routes

# Start development server
php artisan serve
# Visit: http://localhost:8000/api/research-projects
```

### 2. Create Controllers
```bash
# Generate API controllers
php artisan make:controller API/ResearchProjectController --api
php artisan make:controller API/LiteratureSearchController --api
php artisan make:controller API/DataExtractionController --api
php artisan make:controller API/MetaAnalysisController --api
php artisan make:controller API/ManuscriptController --api
php artisan make:controller API/UserController --api
```

### 3. Test Database Connection
```bash
# Run a simple query test
php artisan tinker
# Type: User::count()  # Should return 0
# Type: exit
```

---

## 🚀 Production Deployment Preparation

### Environment Variables
```bash
# Production .env settings
APP_ENV=production
APP_KEY=your_app_key_here
DB_HOST=your_production_db_host
DB_DATABASE=research_automation_prod
DB_USERNAME=your_prod_username
DB_PASSWORD=your_prod_password

# Security
SANCTUM_STATEFUL_DOMAINS=yourdomain.com,www.yourdomain.com
SESSION_DOMAIN=.yourdomain.com
```

### Web Server Configuration
```bash
# Apache .htaccess or Nginx config
# Point document root to /public directory
# Enable URL rewriting for API routes
```

---

## 🔥 Ready for Global Research Transformation

**Your enterprise research automation platform is now technically ready to:**

✅ **Accelerate Systematic Reviews** from weeks to days
✅ **Enable Multi-Institutional Collaboration** globally
✅ **Automate Meta-Analysis** with statistical precision
✅ **Generate Manuscripts** with AI-powered assistance
✅ **Ensure Research Integrity** through automated validation
✅ **Scale Research Productivity** by 10x

**The research world is ready for this transformation. Let's continue building the future of research automation!** 🚀
