const form = document.querySelector("#login-form"); //html에서 form 가져오기

//password 1,2를 가져오고 + 같은지 비교하는 함수
//new FormData(): HTML for 요소를 가져오는 클래스. 서버로 전송할 떄 사용.
//.get()은 FormData에 저장된 값을 가져오는 메서드.
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  //밑에 if 조건문 있는데, 여기서 하는 이유는??
  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  //id, 패스워드 제출시 이벤트
  event.preventDefault(); //자동 리프레시 방지
  const formData = new FormData(form); //formData에서 id와 password 값을 가져와서
  const sha256Password = sha256(formData.get("password")); //formData에서  password 값을 sha256으로 감싸고
  formData.set("password", sha256Password); //원래 password를 sha256으로 감싼 password로 대체한다.

  //서버로 요청 보냄
  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });
  const data = await res.json(); //파이썬의 login 응답을 받아옴
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인 되었습니다.");

  window.location.pathname = "/";

  // console.log("액세스 토큰!", data); //파이썬의 액세스 토큰 응답을 받아옴
  // if (res.status === 200) {
  //   alert("로그인에 성공했습니다.");
  //   window.location.pathname = "/"; //알림 누르면 메인페이지로 이동
  // } else if (res.status === 401) {
  //   alert("id 또는 password가 올바르지 않습니다.");
  // }
};

form.addEventListener("submit", handleSubmit); //id, 패스워드 제출행위
