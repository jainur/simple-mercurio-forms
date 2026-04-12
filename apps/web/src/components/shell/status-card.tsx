import type { ReadyStatus } from "@/types/api";

type StatusCardProps = {
  status: ReadyStatus;
};

export function StatusCard({ status }: StatusCardProps) {
  const pillClassName =
    status.kind === "success"
      ? "bg-emerald-100 text-emerald-800"
      : status.kind === "degraded"
        ? "bg-amber-100 text-amber-900"
        : "bg-slate-200 text-slate-700";

  return (
    <aside className="rounded-[2rem] border border-black/5 bg-white/80 p-7 shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
            API readiness
          </p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">
            Backend connectivity check
          </h2>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-medium ${pillClassName}`}>
          {status.label}
        </span>
      </div>

      <p className="mt-4 text-base leading-7 text-slate-700">{status.message}</p>

      <dl className="mt-6 space-y-3 text-sm text-slate-600">
        <div className="flex items-center justify-between gap-4 rounded-2xl bg-slate-50 px-4 py-3">
          <dt>Configured API base URL</dt>
          <dd className="font-medium text-slate-900">{status.baseUrl}</dd>
        </div>
        <div className="flex items-center justify-between gap-4 rounded-2xl bg-slate-50 px-4 py-3">
          <dt>Health endpoint</dt>
          <dd className="font-medium text-slate-900">/health/ready</dd>
        </div>
      </dl>
    </aside>
  );
}