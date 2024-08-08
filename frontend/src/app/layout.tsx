import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import QueryProvider from "@/context/QueryProvider";

import NavbarLayout from "@/components/ui/NavbarLayout";
import Navbar from "@/components/ui/Navbar";

const poppins = Poppins({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-poppins",
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "Recepies Shopping List",
  description:
    "Find recipes and generate a shopping list for your weekly menu helping you reducing waste and improving your savings still saving you time.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={poppins.className}>
        <QueryProvider>
          <main style={{ display: "flex" }}>
            <NavbarLayout />
            {children}
          </main>
        </QueryProvider>
      </body>
    </html>
  );
}
