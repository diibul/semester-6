# Phase 5 - Testing and Quality Assurance

Dokumen ini merekap hasil pengujian untuk checklist Phase 5 roadmap.

## 1) End-to-End dan functional scenario

Scenario yang tervalidasi:
- Register -> Login -> Booking -> Dummy payment -> Confirmed status.
- User create forum post -> create comment -> data tampil di UI.

Functional matrix:
- Login valid dan invalid: pass.
- Booking double booking: pass.
- Forum spam input (oversized payload): pass.

## 2) Edge case testing

- Booking saat jadwal penuh (is_available false): pass.
- Input kosong (booking/form forum): pass.
- SQL injection basic pada login payload: pass (tetap guest, tidak bypass auth).

## 3) Performance checks

- Query tidak berat (bounded query check pada studio index): pass.
- N+1 problem: pass (forum index diuji dengan lazy loading prevention, tidak terjadi lazy-loading error).

## 4) Bukti uji (command log ringkas)

Dijalankan di folder `backend`:

- `php vendor/bin/phpunit tests/Feature/Phase5EdgeCaseTest.php --testdox`
  - Result: OK (4 tests, 15 assertions)

- `php vendor/bin/phpunit tests/Feature/PerformanceQueryTest.php --testdox`
  - Result: OK (2 tests, 4 assertions)

- `php vendor/bin/phpunit tests/Feature/BookingFeatureTest.php tests/Feature/ForumFeatureTest.php tests/Feature/Auth/AuthenticationTest.php --testdox`
  - Result: OK (9 tests, 29 assertions)

Total evidence suite: 15 tests, 48 assertions, all pass.

## 5) Cross device/browser

- Chrome: diuji melalui responsive layout dan build verification.
- Edge: perlu uji manual browser runtime (belum dijalankan otomatis dari CLI).
- Mobile browser: perlu uji manual di device nyata.

Catatan:
Uji Edge dan mobile browser memerlukan validasi manual visual-interaktif yang tidak dapat dipastikan penuh hanya dari terminal test suite.

## 6) File test yang ditambahkan untuk Phase 5

- `backend/tests/Feature/Phase5EdgeCaseTest.php`
- `backend/tests/Feature/PerformanceQueryTest.php`

## 7) Kesimpulan

Status Phase 5: Completed (automated test scope).

Poin manual lanjutan yang direkomendasikan:
- Smoke test di Microsoft Edge.
- Smoke test di mobile browser langsung pada perangkat.
