import PublicLayout from '@/Layouts/PublicLayout';
import { Head, Link } from '@inertiajs/react';

export default function Welcome() {
    const highlights = [
        {
            title: 'Cari studio favorit',
            description: 'Bandingkan studio dengan cepat dan temukan tempat latihan yang cocok untuk gaya musikmu.',
            icon: (
                <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <circle cx="11" cy="11" r="7" />
                    <path d="M20 20l-3.5-3.5" strokeLinecap="round" />
                </svg>
            ),
        },
        {
            title: 'Pilih jadwal yang pas',
            description: 'Cek slot yang tersedia, pilih waktu latihan, lalu lanjut booking tanpa alur yang rumit.',
            icon: (
                <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <rect x="3" y="4" width="18" height="17" rx="2" />
                    <path d="M8 2v4M16 2v4M3 9h18" strokeLinecap="round" />
                </svg>
            ),
        },
        {
            title: 'Terhubung lewat diskusi musik',
            description: 'Diskusi musik dan terhubung dengan musisi lain. Berbagi pengalaman dan insight setelah sesi latihan.',
            icon: (
                <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <path d="M4 5h16v10H8l-4 4V5z" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
            ),
        },
    ];

    return (
        <PublicLayout title="Welcome" showIntro={false}>
            <Head title="Welcome" />

            <div className="grid items-stretch gap-6 lg:grid-cols-[1.15fr_0.85fr]">
                <section className="rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-black/20 sm:p-10">
                    <p className="text-sm uppercase tracking-[0.3em] text-cyan-300">StudioBook</p>
                    <h1 className="mt-4 max-w-2xl text-4xl font-bold leading-tight text-white sm:text-6xl">
                        Booking studio musik tanpa ribet dalam satu platform.
                    </h1>
                    <p className="mt-5 max-w-2xl text-base leading-7 text-white/70">
                        Cari, pilih jadwal, dan booking dalam hitungan menit.
                    </p>

                    <div className="mt-8">
                        <Link
                            href={route('studios.index')}
                            className="inline-flex rounded-full bg-cyan-300 px-7 py-3 text-base font-semibold text-slate-950 transition hover:bg-cyan-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-200"
                        >
                            Mulai Booking
                        </Link>
                    </div>

                    <div className="mt-7 flex flex-wrap gap-3 text-sm text-white/80">
                        <span className="rounded-full border border-white/15 bg-white/10 px-4 py-2">Digunakan oleh 100+ musisi</span>
                        <span className="rounded-full border border-white/15 bg-white/10 px-4 py-2">Booking cepat & mudah</span>
                    </div>
                </section>

                <aside className="grid gap-4">
                    <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/5">
                        <img
                            src="https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=1200&q=80"
                            alt="Ruang studio musik"
                            className="h-56 w-full object-cover sm:h-64"
                            loading="lazy"
                        />
                    </div>

                    <div className="rounded-3xl bg-cyan-400/10 p-6 ring-1 ring-cyan-300/20">
                        <p className="text-sm uppercase tracking-[0.25em] text-cyan-200">User Flow</p>
                        <ol className="mt-4 list-decimal space-y-2 pl-5 text-sm leading-6 text-white/80 marker:text-cyan-200">
                            <li>Cari studio.</li>
                            <li>Pilih jadwal.</li>
                            <li>Booking dan gunakan.</li>
                        </ol>
                    </div>
                </aside>
            </div>

            <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {highlights.map((item) => (
                    <div key={item.title} className="rounded-2xl border border-white/10 bg-white/5 p-6">
                        <div className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-cyan-300/20 text-cyan-200">
                            {item.icon}
                        </div>
                        <h3 className="mt-4 text-lg font-semibold text-white">{item.title}</h3>
                        <p className="mt-2 text-sm leading-6 text-white/75">{item.description}</p>
                    </div>
                ))}
            </div>
        </PublicLayout>
    );
}
