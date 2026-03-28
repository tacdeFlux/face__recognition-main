import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar";
import { ClerkProvider } from "@clerk/nextjs";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Face Recognition",
  description: "Based on the attendence",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <html lang="en" className="dark">
        <body className={inter.className}>
           <ClerkProvider dynamic>
          <div className="relative w-full flex items-center justify-center">
            <Navbar />
          </div>
          {children}
          </ClerkProvider>
        </body>
      </html>
  );
}
