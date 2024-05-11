<script>
  import { onMount } from "svelte";
  import Footer from "../components/Nav.svelte";
  import { getDatabase, ref, onValue } from "firebase/database";
  import Nav from "../components/Nav.svelte";
  // 타이머 만들기
  let hour = new Date().getHours();
  let min = new Date().getMinutes();

  //랜더링 반응 어쩌고..
  $: items = [];

  //Main창에 표시할 시간
  const calcTime = (timestamp) => {
    const curTime = new Date().getTime() - 7 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp);
    const hour = time.getHours();
    const minute = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second > 0) return `${second}초 전`;
    else return "방금 전";
  };

  const db = getDatabase();
  const itemsRef = ref(db, "items/");

  //onMount: 상시표시 내용
  onMount(() => {
    onValue(itemsRef, (snapshot) => {
      const data = snapshot.val();
      items = Object.values(data).reverse(); //최신순으로 나열
    });
  });
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
  <!--Main창 표시 정보-->
  {#each items as item}
    <div class="item-list">
      <div class="item-list__img">
        <img alt={item.title} src={item.imgUrl} />
      </div>
      <div class="item-list__info">
        <div class="item-list__info-title">{item.title}</div>
        <div class="item-list_info-meta">
          {item.place}{calcTime(item.insertAt)}
        </div>
        <div class="item-list_info-price">{item.price}</div>
        <div class="item-list_info-decription">{item.description}</div>
      </div>
    </div>
  {/each}
  <a class="write-btn" href="#/write">+글쓰기</a>
</main>

<!--components_Footer.svelte에서 가져옴-->
<Nav location="home" />

<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>

<style>
  /* CSS도 기존 작성양식 대로 입력하면 됨 */
  .info-bar__time {
    color: blue;
  }
</style>
