<?php

use App\Models\Studio;
use Illuminate\Support\Facades\Route;

Route::get('/studios', function () {
	$studios = Studio::query()
		->withCount(['schedules as available_schedules_count' => function ($query) {
			$query->where('is_available', true);
		}])
		->with(['schedules' => function ($query) {
			$query->where('is_available', true)
				->orderBy('schedule_date')
				->orderBy('start_time');
		}])
		->latest()
		->get();

	return response()->json([
		'data' => $studios,
	]);
});

Route::get('/studios/{studio:slug}', function (Studio $studio) {
	$studio->load([
		'schedules' => function ($query) {
			$query->where('is_available', true)
				->orderBy('schedule_date')
				->orderBy('start_time');
		},
	]);

	return response()->json([
		'data' => $studio,
	]);
});
