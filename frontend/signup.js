const form = document.querySelector("#signup-form"); //html에서 form 가져오기

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

const handleSubmitForm = async (event) => {
  //id, 패스워드 제출시 이벤트
  event.preventDefault(); //자동 리프레시 방지
  const formData = new FormData(form); //formData에서 id와 password 값을 가져와서
  const sha256Password = sha256(formData.get("password")); //formData에서  password 값을 sha256으로 감싸고
  formData.set("password", sha256Password); //원래 password를 sha256으로 감싼 password로 대체한다.

  const div = document.querySelector("#info"); //true, false에 표시할 안내문 div

  //password 체크 요청 보내기
  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });

    const data = await res.json(); //서버로부터 체크 데이터를 받았는데
    //그 데이터가 200이었을 때,
    if (data === "200") {
      alert("회원 가입에 성공했습니다."); //200되어서 회원가입 성공하면, alert 나옴
      window.location.pathname = "/login.html"; // alert 확인하면, /login.html(로그인)창으로 이동
    }
  } else {
    //200 아닐 때
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmitForm); //id, 패스워드 제출행위
