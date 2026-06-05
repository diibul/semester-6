<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('alumni', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('nim')->unique();
            $table->string('study_program');
            $table->unsignedSmallInteger('graduation_year');
            $table->string('email')->nullable();
            $table->enum('tracking_status', [
                'Belum Dilacak',
                'Teridentifikasi',
                'Perlu Verifikasi',
                'Belum Ditemukan',
            ])->default('Belum Dilacak');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('alumni');
    }
};
