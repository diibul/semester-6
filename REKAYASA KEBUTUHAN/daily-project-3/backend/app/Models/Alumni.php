<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Alumni extends Model
{
    use HasFactory;

    protected $table = 'alumni';

    protected $fillable = [
        'name',
        'nim',
        'entry_year',
        'graduation_date',
        'faculty',
        'study_program',
        'graduation_year',
        'email',
        'social_media_linkedin',
        'social_media_instagram',
        'social_media_facebook',
        'social_media_tiktok',
        'phone_number',
        'workplace_name',
        'workplace_address',
        'position',
        'employment_type',
        'workplace_social_media',
        'tracking_status',
    ];

    public function trackingResults(): HasMany
    {
        return $this->hasMany(TrackingResult::class);
    }
}
