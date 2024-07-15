"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import axios from "axios";
import Image from "next/image";
import google from "../../../../public/svg/google.svg";
import facebook from "../../../../public/svg/facebook.svg";
import apple from "../../../../public/svg/apple.svg";
import heroImg from "../../../../public/svg/login_image.svg";
import styles from "./LoginComp.module.css";

interface FormType {
  email: string;
  password: string;
}
export default function LoginComp() {
  const router = useRouter();
  const [userCredentials, setUserCredentials] = useState<FormType>({
    email: "",
    password: "",
  });

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setUserCredentials({
      ...userCredentials,
      [name]: value,
    });
  }

  async function handleSignIn(e: any) {
    e.preventDefault();
    const { email, password } = userCredentials;
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded",
    };
    try {
      // check if input not empty
      if (email && password) {
        const userData = {
          email,
          password,
        };
        const data = await axios.post(
          "https://v50-tier3-team-22.onrender.com/token",
          userData,
          { headers: headers }
        );
        // let {
        //   data: { session },
        //   error,
        // } = await supabase.auth.signInWithPassword({
        //   email: userCredentials.email.toLowerCase(),
        //   password: userCredentials.password,
        // });
        // if (error) {
        //   throw error;
        // }
        // if (session) {
        //   router.replace("/");
        // }
        console.log(data);
      }
    } catch (error: unknown) {
      console.error(error);
    }
    setUserCredentials({ ...userCredentials, password: "" });
  }

  return (
    <div className={styles["main__container"]}>
      <section className={styles.container}>
        <section className={styles.box}>
          <div className={styles["text__box"]}>
            <h1>Welcome Back!</h1>
            <p className={styles.slug}>
              Enter your Credentials to access your account{" "}
            </p>
            <form onSubmit={handleSignIn}>
              <label htmlFor="email">Email address</label>
              <input
                type="email"
                name="email"
                placeholder="enter your email"
                value={userCredentials.email}
                onChange={handleInputChange}
                required
              />
              <Link href={""}>
                <p className={styles["forgot__pass"]}>forgot password?</p>
              </Link>
              <label htmlFor="password">Password</label>
              <input
                type="password"
                name="password"
                placeholder="password"
                value={userCredentials.password}
                onChange={handleInputChange}
                required
              />
              <p className={styles["check__box"]}>
                <input type="checkbox" /> Remember for 30days
              </p>
              <button type="submit">Login</button>
            </form>
          </div>

          <div>
            <p className={styles.division}>or</p>
          </div>

          <div className={styles["button__box"]}>
            <div>
              <button>
                <Image src={google} layout="responsive" alt="" />
                sign in with google
              </button>
              <button>
                <Image src={apple} layout="responsive" alt="" />
                sign in with apple
              </button>
            </div>
            <div>
              <button>
                <Image src={facebook} layout="responsive" width={2} alt="" />
                sign in with facebook
              </button>
            </div>
          </div>
          <div className={styles["signup__text"]}>
            <p>Don't have an account?</p>
            <Link href={""}>Sign up</Link>
          </div>
        </section>
        <div className={styles["image__box"]}>
          <div>
            {/* <Image src={heroImg} layout="responsive" alt="" />{" "} */}
          </div>
        </div>
      </section>
    </div>
  );
}
