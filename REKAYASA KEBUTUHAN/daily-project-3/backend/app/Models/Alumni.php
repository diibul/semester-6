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
        'study_program',
        'graduation_year',
        'email',
        'tracking_status',
    ];

    public function trackingResults(): HasMany
    {
        return $this->hasMany(TrackingResult::class);
    }
}
