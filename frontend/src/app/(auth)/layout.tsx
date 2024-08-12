import SideNavbar from "@/components/Layout/navbbar/SideNavbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-full min-h-screen flex-row w-full">{children}</div>
  );
}
