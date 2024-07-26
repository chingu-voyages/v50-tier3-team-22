import SideNavbar from "@/components/Layout/navbbar/SideNavbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-full min-h-screen flex-row py-14">
      <div className="flex flex-col gap-16 w-1/6 h-full px-4 ">
        <h1 className="text-4xl font-medium">Logo</h1>
        <SideNavbar />
      </div>
      {children}
    </div>
  );
}
