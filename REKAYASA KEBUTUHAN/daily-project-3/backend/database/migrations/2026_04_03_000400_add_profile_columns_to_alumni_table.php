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
        Schema::table('alumni', function (Blueprint $table) {
            $table->unsignedSmallInteger('entry_year')->nullable()->after('nim');
            $table->date('graduation_date')->nullable()->after('entry_year');
            $table->string('faculty')->nullable()->after('graduation_date');

            $table->string('social_media_linkedin')->nullable()->after('email');
            $table->string('social_media_instagram')->nullable()->after('social_media_linkedin');
            $table->string('social_media_facebook')->nullable()->after('social_media_instagram');
            $table->string('social_media_tiktok')->nullable()->after('social_media_facebook');
            $table->string('phone_number')->nullable()->after('social_media_tiktok');
            $table->string('workplace_name')->nullable()->after('phone_number');
            $table->text('workplace_address')->nullable()->after('workplace_name');
            $table->string('position')->nullable()->after('workplace_address');
            $table->enum('employment_type', ['PNS', 'Swasta', 'Wirausaha'])->nullable()->after('position');
            $table->string('workplace_social_media')->nullable()->after('employment_type');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('alumni', function (Blueprint $table) {
            $table->dropColumn([
                'entry_year',
                'graduation_date',
                'faculty',
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
            ]);
        });
    }
};
