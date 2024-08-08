import Link from "next/link";
import styles from "./Navbar.module.css";
export default function Navbar() {
  return (
    <nav className={styles.container}>
      <h2> Logo </h2>
      <ul>
        <li>
          <Link href="/">Home</Link>
        </li>
        <li>
          <Link href="/recipe">Recipe </Link>
        </li>
        <li>
          <Link href="/">Shopping List </Link>
        </li>
        <li>
          <Link href="/mealsplan">Meal Plan </Link>
        </li>
        <li>
          <Link href="">Favourites </Link>
        </li>
      </ul>
    </nav>
  );
}
