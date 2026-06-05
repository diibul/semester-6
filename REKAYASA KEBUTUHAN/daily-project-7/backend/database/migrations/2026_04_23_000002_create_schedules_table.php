<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('schedules', function (Blueprint $table) {
            $table->id();
            $table->foreignId('studio_id')->constrained()->cascadeOnDelete();
            $table->date('schedule_date');
            $table->time('start_time');
            $table->time('end_time');
            $table->boolean('is_available')->default(true);
            $table->timestamps();

            $table->unique(['studio_id', 'schedule_date', 'start_time', 'end_time'], 'studio_schedule_unique');
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('schedules');
    }
};