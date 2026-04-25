<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Support\Str;

class Studio extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'name',
        'slug',
        'type',
        'description',
        'location',
        'price_per_hour',
        'image_url',
    ];

    protected $casts = [
        'price_per_hour' => 'decimal:2',
    ];

    protected static function booted(): void
    {
        static::creating(function (Studio $studio): void {
            if (empty($studio->slug)) {
                $studio->slug = Str::slug($studio->name);
            }
        });
    }

    public function getRouteKeyName(): string
    {
        return 'slug';
    }

    public function schedules(): HasMany
    {
        return $this->hasMany(Schedule::class);
    }

    public function owner(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function bookings(): HasMany
    {
        return $this->hasMany(Booking::class);
    }
}
