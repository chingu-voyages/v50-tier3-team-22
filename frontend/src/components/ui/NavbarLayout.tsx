import { ReactNode, useState } from "react";
import Navbar from "./Navbar";

type LayoutProps = {
  children?: ReactNode;
};

export default function NavbarLayout(props: LayoutProps) {
  return (
    <div>
      <Navbar />
      <main style={{ width: "80%", backgroundColor: "black" }}>
        {props.children}
      </main>
    </div>
  );
}
