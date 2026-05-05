import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Project Leap Cockpit",
  description: "Agentic executive cockpit for Shriram Farm Solutions",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
