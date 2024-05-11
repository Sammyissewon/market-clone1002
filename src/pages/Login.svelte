<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  //구글 로그인 팝업 만들기
  const provider = new GoogleAuthProvider();
  const auth = getAuth();

  const loginWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      const credential = GoogleAuthProvider.credentialFromResult(result); //구글의 인증정보를 가져오고
      const token = credential.accessToken; // 그 인증정보는 엑세스 토큰을 담고
      const user = result.user; // 유저 정보도 담고
      user$.set(user);
      localStorage.setItem("token", token);
    } catch (error) {
      //오류 잡기
      console.error(error);
    }
  };
</script>

<div>
  <div>로그인하기</div>
  <button class="login-btn" on:click={loginWithGoogle}>
    <img
      class="google-img"
      src="https://cdn1.iconfinder.com/data/icons/google-s-logo/150/Google_Icons-09-512.png"
      alt=""
    />
    <div>Google로 시작하기</div>
    <div />
  </button>
</div>

<style>
  .login-btn {
    width: 300px;
    height: 50px;
    border: 1px solid grey;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    border-radius: 3px;
  }

  .google-img {
    width: 40px;
  }
</style>
