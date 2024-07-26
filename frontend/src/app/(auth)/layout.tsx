import SideNavbar from "@/components/Layout/navbbar/SideNavbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-full min-h-screen flex-row ">
      <div className="flex flex-col gap-16 w-1/6 px-4 py-14 bg-white">
        <h1 className="text-4xl font-medium">Logo</h1>
        <SideNavbar />
      </div>
      {children}
    </div>
  );
}
