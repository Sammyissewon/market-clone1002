<script>
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Router from "svelte-spa-router"; //Router 태그 삽입
  import "./CSS/18.style.css"; //기존 CSS파일을 모두 src_CSS 폴더로 이동

  //기존 사진 소스는 public 폴더로 이동

  //Router 설정
  //URL에 #/ 붙이기 -> http://localhost:5173/#/login
  const routes = {
    "/": Main,
    "/login": Login,
    "/signup": Signup,
    "/write": Write,
    "*": NotFound,
  };
</script>

<Router {routes} />

<main></main>

<style>
</style>
