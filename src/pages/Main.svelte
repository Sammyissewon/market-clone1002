<script>
  // 타이머 만들기
  let hour = new Date().getHours();
  let min = new Date().getMinutes();
</script>

<header>
  <div class="info-bar">
    <!--위에 let 가져옴-->
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="18.resource/chart.svg" alt="chart" />
      <img src="18.resource/wifi.svg" alt="chart" />
      <img src="18.resource/battery.svg" alt="chart" />
    </div>
  </div>

  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar__location-icon">
        <img src="18.resource/arrow.svg" alt="" />
      </div>
    </div>

    <div class="menu-bar__icons">
      <img src="18.resource/search.svg" alt="" />
      <img src="18.resource/menu.svg" alt="" />
      <img src="18.resource/alert.svg" alt="" />
    </div>
  </div>
</header>

<main>
  <a class="write-btn" href="#/write">+글쓰기</a>
</main>

<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>

<footer>
  <div class="footer-block">
    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="18.resource/home.svg" />
      </div>
      <div>홈</div>
    </div>

    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="18.resource/docu.svg" />
      </div>
      <div>동네생활</div>
    </div>

    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="18.resource/location.svg" />
      </div>
      <div>내 근처</div>
    </div>

    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="18.resource/chat.svg" />
      </div>
      <div>채팅</div>
    </div>

    <div class="footer-icons">
      <div class="footer-icons__img">
        <img src="18.resource/user.svg" />
      </div>
      <div>나의당근</div>
    </div>
  </div>
</footer>

<style>
  /* CSS도 기존 작성양식 대로 입력하면 됨 */
  .info-bar__time {
    color: blue;
  }
</style>
