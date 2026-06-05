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
        Schema::create('tracking_results', function (Blueprint $table) {
            $table->id();
            $table->foreignId('alumni_id')->constrained('alumni')->cascadeOnDelete();
            $table->string('source');
            $table->string('title');
            $table->text('description')->nullable();
            $table->string('url', 2048)->nullable();
            $table->decimal('confidence_score', 5, 2)->default(0);
            $table->string('status')->default('Perlu Verifikasi');
            $table->timestamp('tracked_at')->nullable();
            $table->timestamp('created_at')->useCurrent();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('tracking_results');
    }
};
