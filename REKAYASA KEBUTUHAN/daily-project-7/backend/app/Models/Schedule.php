<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasOne;

class Schedule extends Model
{
    use HasFactory;

    protected $fillable = [
        'studio_id',
        'schedule_date',
        'start_time',
        'end_time',
        'is_available',
    ];

    protected $casts = [
        'schedule_date' => 'date',
        'is_available' => 'boolean',
    ];

    public function studio(): BelongsTo
    {
        return $this->belongsTo(Studio::class);
    }

    public function booking(): HasOne
    {
        return $this->hasOne(Booking::class);
    }
}