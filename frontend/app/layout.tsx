import type { Metadata } from "next";
import Link from "next/link";
import { Inter } from "next/font/google";
import "./globals.css";

// Load the Geist fonts from Google Fonts.
// Apply varibale font throughout the app via CSS variables
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});



// Metadata controls the browser tab title and page description
export const metadata: Metadata = {
  title: "Risk Assessment App",
  description: "Analyze crime, weather, disaster, and population risk by ZIP code",
};

// RootLayout
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // Apply global font styling to HTML document
    <html lang="en" className={inter.variable}>
      {/* Body */}
      <body className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
        {/* Navigation Bar */}
        <nav className="bg-white/70 backdrop-blur border-b border-slate-200">
          <div className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">

            {/* Application title */}
            <h1 className="text-xl font-semibold tracking-tight">
              Risk Assessment App
            </h1>

            {/* Navigation links */}
            <div className="flex gap-6 text-md font-medium">

              <Link
                href="/"
                className="text-slate-600 hover:text-slate-900 transition"
              >
                Dashboard
              </Link>

              <Link
                href="/history"
                className="text-slate-600 hover:text-slate-900 transition"
              >
                History
              </Link>

            </div>
          </div>
        </nav>

        {/* Page Content */}
        <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}