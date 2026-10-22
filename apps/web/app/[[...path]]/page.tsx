import { notFound } from "next/navigation";
import { cookies } from "next/headers";
import { NourApp } from "@/components/nour-app";

export default async function Page({
  params,
}: {
  params: Promise<{ path?: string[] }>;
}) {
  const path = (await params).path?.join("/") || "";
  if (!["", "diary", "recipes", "profile"].includes(path)) notFound();
  const locale =
    (await cookies()).get("nour_locale")?.value === "ar" ? "ar" : "en";
  return <NourApp initialLocale={locale} />;
}
