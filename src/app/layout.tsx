import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import { isDcmshriramSite } from "@/lib/site-variant";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-inter",
  display: "swap",
});

const fraunces = Fraunces({
  subsets: ["latin"],
  weight: ["400", "500"],
  style: ["normal", "italic"],
  variable: "--font-fraunces",
  display: "swap",
});

const jetBrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

const conformalMetadata: Metadata = {
  metadataBase: new URL("https://conformal.live"),
  title: " ",
  description: "",
  applicationName: "Conformal",
  alternates: {
    canonical: "/",
  },
  robots: {
    index: false,
    follow: false,
  },
};

const dcmshriramMetadata: Metadata = {
  metadataBase: new URL("https://dcmshriram.conformal.live"),
  title: "Conformal Cockpit",
  description: "Executive cockpit for Shriram Farm Solutions",
  applicationName: "Conformal Cockpit",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Conformal Cockpit",
    description: "Executive cockpit for Shriram Farm Solutions",
    url: "https://dcmshriram.conformal.live/",
    siteName: "Shriram Farm Solutions",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Conformal Cockpit",
    description: "Executive cockpit for Shriram Farm Solutions",
  },
};

export const metadata: Metadata = isDcmshriramSite() ? dcmshriramMetadata : conformalMetadata;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${fraunces.variable} ${jetBrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
