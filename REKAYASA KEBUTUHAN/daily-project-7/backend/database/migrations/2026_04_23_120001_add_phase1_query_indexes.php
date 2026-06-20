<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('schedules', function (Blueprint $table) {
            $table->index('schedule_date', 'schedules_schedule_date_idx');
        });

        Schema::table('bookings', function (Blueprint $table) {
            $table->index('booking_status', 'bookings_booking_status_idx');
            $table->index('payment_status', 'bookings_payment_status_idx');
        });
    }

    public function down(): void
    {
        Schema::table('bookings', function (Blueprint $table) {
            $table->dropIndex('bookings_booking_status_idx');
            $table->dropIndex('bookings_payment_status_idx');
        });

        Schema::table('schedules', function (Blueprint $table) {
            $table->dropIndex('schedules_schedule_date_idx');
        });
    }
};
