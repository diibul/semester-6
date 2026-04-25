import InputError from '@/Components/InputError';
import PrimaryButton from '@/Components/PrimaryButton';
import TextInput from '@/Components/TextInput';
import PublicLayout from '@/Layouts/PublicLayout';
import { Head, Link, useForm, usePage } from '@inertiajs/react';

export default function Show({ studio }) {
    const user = usePage().props.auth.user;
    const flash = usePage().props.flash;
    const formatDate = (value) => String(value).slice(0, 10);
    const { data, setData, post, processing, errors, reset } = useForm({
        studio_id: studio.id,
        schedule_id: '',
        booking_date: '',
        notes: '',
    });

    const submit = (e) => {
        e.preventDefault();

        post(route('bookings.store'), {
            preserveScroll: true,
            onSuccess: () => reset('schedule_id', 'booking_date', 'notes'),
        });
    };

    const selectedSchedule = studio.schedules.find(
        (schedule) => String(schedule.id) === String(data.schedule_id),
    );

    return (
        <PublicLayout title={studio.name}>
            <Head title={studio.name} />

            {flash.success && (
                <div className="mb-6 rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
                    {flash.success}
                </div>
            )}

            {flash.error && (
                <div className="mb-6 rounded-xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
                    {flash.error}
                </div>
            )}

            <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
                <article className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20">
                    <div className="flex flex-wrap items-center gap-3 text-sm text-white/60">
                        <span className="rounded-full bg-cyan-400/15 px-3 py-1 text-cyan-200">{studio.type}</span>
                        <span>{studio.location}</span>
                    </div>

                    <p className="mt-5 text-base leading-7 text-white/75">{studio.description}</p>

                    <div className="mt-6 rounded-2xl bg-black/20 p-4">
                        <p className="text-sm uppercase tracking-[0.25em] text-cyan-300">Harga</p>
                        <p className="mt-2 text-2xl font-semibold text-white">Rp {studio.price_per_hour} / jam</p>
                    </div>

                    <div className="mt-8">
                        <h3 className="text-lg font-semibold text-white">Jadwal tersedia</h3>
                        <div className="mt-4 grid gap-3">
                            {studio.schedules.map((schedule) => {
                                const isBooked = Boolean(schedule.booking) || !schedule.is_available;
                                return (
                                    <label
                                        key={schedule.id}
                                        className={`flex cursor-pointer items-center justify-between rounded-xl border px-4 py-3 transition ${
                                            String(data.schedule_id) === String(schedule.id)
                                                ? 'border-cyan-300 bg-cyan-300/10'
                                                : 'border-white/10 bg-white/5 hover:border-white/20'
                                        } ${isBooked ? 'opacity-60' : ''}`}
                                    >
                                        <div>
                                            <div className="text-sm font-semibold text-white">
                                                {formatDate(schedule.schedule_date)} | {schedule.start_time} - {schedule.end_time}
                                            </div>
                                            <div className="text-xs text-white/60">
                                                {isBooked ? 'Sudah dibooking' : 'Tersedia'}
                                            </div>
                                        </div>
                                        <input
                                            type="radio"
                                            name="schedule_id"
                                            value={schedule.id}
                                            disabled={isBooked}
                                            checked={String(data.schedule_id) === String(schedule.id)}
                                            onChange={(event) => {
                                                const nextSchedule = studio.schedules.find(
                                                    (item) => String(item.id) === String(event.target.value),
                                                );
                                                setData('schedule_id', event.target.value);
                                                setData('booking_date', nextSchedule ? formatDate(nextSchedule.schedule_date) : '');
                                            }}
                                        />
                                    </label>
                                );
                            })}
                        </div>
                    </div>
                </article>

                <aside className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/20">
                    <h3 className="text-lg font-semibold text-white">Booking cepat</h3>
                    <p className="mt-2 text-sm text-white/60">Pilih jadwal, isi catatan singkat, lalu submit booking.</p>

                    {user ? (
                        <form onSubmit={submit} className="mt-6 space-y-4">
                            <div>
                                <label className="text-sm font-medium text-white/80">Tanggal booking</label>
                                <TextInput
                                    type="date"
                                    className="mt-1 block w-full border-white/10 bg-white/10 text-white"
                                    value={data.booking_date}
                                    onChange={(event) => setData('booking_date', event.target.value)}
                                />
                                <InputError message={errors.booking_date} className="mt-2" />
                            </div>

                            <div>
                                <label className="text-sm font-medium text-white/80">Catatan</label>
                                <textarea
                                    className="mt-1 block w-full rounded-md border-white/10 bg-white/10 text-white shadow-sm focus:border-cyan-300 focus:ring-cyan-300"
                                    rows="4"
                                    value={data.notes}
                                    onChange={(event) => setData('notes', event.target.value)}
                                />
                                <InputError message={errors.notes} className="mt-2" />
                            </div>

                            <InputError message={errors.schedule_id} className="mt-2" />

                            {selectedSchedule && (
                                <div className="rounded-xl bg-black/20 p-4 text-sm text-white/70">
                                    Jadwal dipilih: {formatDate(selectedSchedule.schedule_date)} {selectedSchedule.start_time} - {selectedSchedule.end_time}
                                </div>
                            )}

                            <PrimaryButton disabled={processing || !data.schedule_id || !data.booking_date} className="w-full justify-center bg-cyan-400 text-slate-950 hover:bg-cyan-300 focus:ring-cyan-300">
                                {processing ? 'Memproses...' : 'Booking sekarang'}
                            </PrimaryButton>
                        </form>
                    ) : (
                        <div className="mt-6 rounded-xl border border-white/10 bg-black/20 p-4">
                            <p className="text-sm text-white/70">Login dulu untuk membuat booking.</p>
                            <Link href={route('login')} className="mt-4 inline-flex rounded-full bg-white px-4 py-2 text-sm font-semibold text-slate-950">
                                Login
                            </Link>
                        </div>
                    )}
                </aside>
            </div>
        </PublicLayout>
    );
}