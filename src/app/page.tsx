import { CockpitShell } from "@/components/CockpitShell";
import { isDcmshriramSite } from "@/lib/site-variant";

export default function Home() {
  if (isDcmshriramSite()) {
    return <CockpitShell />;
  }

  return <main aria-hidden="true" className="min-h-screen bg-white" />;
}
