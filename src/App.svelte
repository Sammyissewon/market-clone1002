<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router"; //Router 태그 삽입
  import "./CSS/18.style.css"; //기존 CSS파일을 모두 src_CSS 폴더로 이동
  import { user$ } from "./store";
  import {
    getAuth,
    GoogleAuthProvider,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import MyPage from "./pages/MyPage.svelte";

  let isLoading = true;

  const auth = getAuth();

  const checkLogin = async () => {
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);

    const credential = GoogleAuthProvider.credential(null, token);
    // Sign in with credential from the Google user.
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    user$.set(user);
    isLoading = false;
  };

  //Router 설정
  //URL에 #/ 붙이기 -> http://localhost:5173/#/login
  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": MyPage,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

{#if isLoading}
  <div>로딩중 입니다.</div>
{:else if !$user$}
  <!--유저 정보가 없을 때는 로그인 화면 보여주기-->
  <Login />
{:else}
  <Router {routes} />
{/if}
