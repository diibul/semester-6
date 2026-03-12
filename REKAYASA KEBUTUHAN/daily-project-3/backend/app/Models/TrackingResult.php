<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class TrackingResult extends Model
{
    use HasFactory;

    public $timestamps = false;

    protected $fillable = [
        'alumni_id',
        'source',
        'title',
        'description',
        'url',
        'confidence_score',
        'status',
        'tracked_at',
        'created_at',
    ];

    protected function casts(): array
    {
        return [
            'confidence_score' => 'float',
            'tracked_at' => 'datetime',
            'created_at' => 'datetime',
        ];
    }

    public function alumni(): BelongsTo
    {
        return $this->belongsTo(Alumni::class);
    }
}
