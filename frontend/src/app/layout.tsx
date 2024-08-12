import type { Metadata } from "next";
import { Poppins } from "next/font/google";
import "./globals.css";
import QueryProvider from "@/context/QueryProvider";

import NavbarLayout from "@/components/ui/NavbarLayout";
import Navbar from "@/components/ui/Navbar";
import SideNavbar from "@/components/Layout/navbbar/SideNavbar";

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
            <div className="flex flex-col gap-16 w-1/6 px-4 py-14 bg-white min-w-48">
              <h1 className="text-4xl font-medium">Logo</h1>
              <SideNavbar />
            </div>
            {children}
          </main>
        </QueryProvider>
      </body>
    </html>
  );
}
