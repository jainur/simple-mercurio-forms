import { AppHeader } from "@/components/shell/app-header";
import { StatusCard } from "@/components/shell/status-card";
import { getReadyStatus } from "@/lib/api/mercurio";

export default async function Home() {
  const status = await getReadyStatus();

  return (
    <div className="flex min-h-screen flex-col bg-[radial-gradient(circle_at_top_left,_rgba(196,181,253,0.18),_transparent_24%),radial-gradient(circle_at_top_right,_rgba(34,197,94,0.16),_transparent_22%),linear-gradient(180deg,_#fffdf7_0%,_#f7f4ea_100%)] text-slate-900">
      <AppHeader />
      <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-10 px-6 py-10 lg:px-10 lg:py-14">
        <section className="grid gap-8 lg:grid-cols-[1.25fr_0.75fr] lg:items-start">
          <div className="space-y-6">
            <p className="inline-flex rounded-full border border-amber-900/10 bg-white/70 px-3 py-1 text-sm font-medium tracking-wide text-amber-950 shadow-sm backdrop-blur">
              Next.js client scaffold
            </p>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
                Web client foundation for form discovery, validation, and PDF filling.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-700">
                This app lives inside the same repository as the FastAPI service but
                remains a separate deployable. Use it as the browser-facing client for
                local installs and SaaS hosting.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              <article className="rounded-3xl border border-black/5 bg-white/75 p-5 shadow-[0_10px_30px_rgba(15,23,42,0.07)] backdrop-blur">
                <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Phase 1
                </h2>
                <p className="mt-3 text-lg font-medium text-slate-900">
                  Forms catalog and field inspection
                </p>
              </article>
              <article className="rounded-3xl border border-black/5 bg-white/75 p-5 shadow-[0_10px_30px_rgba(15,23,42,0.07)] backdrop-blur">
                <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Phase 2
                </h2>
                <p className="mt-3 text-lg font-medium text-slate-900">
                  Validation, preview, and fill flows
                </p>
              </article>
              <article className="rounded-3xl border border-black/5 bg-white/75 p-5 shadow-[0_10px_30px_rgba(15,23,42,0.07)] backdrop-blur">
                <h2 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Phase 3
                </h2>
                <p className="mt-3 text-lg font-medium text-slate-900">
                  Authenticated SaaS and self-hosted packaging
                </p>
              </article>
            </div>
          </div>
          <StatusCard status={status} />
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <article className="rounded-[2rem] border border-black/5 bg-slate-950 p-7 text-slate-50 shadow-[0_20px_60px_rgba(15,23,42,0.18)]">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-300">
              Intended boundary
            </p>
            <h2 className="mt-4 text-2xl font-semibold">Browser app, not API key client</h2>
            <p className="mt-4 max-w-xl text-base leading-7 text-slate-300">
              Keep browser traffic behind Next.js server routes or move to real user
              authentication on the API. Do not expose the current shared API-key
              pattern directly to the browser.
            </p>
          </article>

          <article className="rounded-[2rem] border border-black/5 bg-white/80 p-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-700">
              Suggested next work
            </p>
            <ol className="mt-4 space-y-3 text-base leading-7 text-slate-700">
              <li>1. Add a typed API client from FastAPI OpenAPI.</li>
              <li>2. Build the forms catalog and form detail routes.</li>
              <li>3. Add auth and artifact access rules before public rollout.</li>
            </ol>
          </article>
        </section>
      </main>
    </div>
  );
}
