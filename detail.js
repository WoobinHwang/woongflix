let title = localStorage.getItem("title");
// let id = sessionStorage.getItem("username")
$('#comment-list').empty();

$.ajax({
  type: "POST",
  url: "/find",
  data: { title_give: title },
  success: function (response) {
    let movie_data = response["movie_data"];
    console.log(movie_data);

    let poster = movie_data["img_url"];
    // console.log(poster);
    let title = movie_data["title"];
    let score = movie_data["score"];
    let desc = movie_data["desc"];
    let url = movie_data["url"];
    let genre = movie_data["genre"];

    let temp_html = `<div class="content detail">
                            <input type="image" src="${poster}" width="202" height="290" style="float: left"/>
                            <div class="boxPadding">
                            <h1>${title}</h1>
                            <a href="${url}">영화 보러가기</a>
                            <p>장르: ${genre}</p>
                            <p>⭐️평점 ${score}</p>
                            <p>줄거리</p>
                            <P>${desc}</P>
                          </div>
                          </div>
                          `;

    $("#movie_detail").append(temp_html);
  },
});

// function get_comments() {}
//comment 받아오기
$.ajax({
  type: "POST",
  url: "/comments",
  data: {title_give: title},
  success: function (response) {
    let comment_data = response["target_comments"];
    console.log(comment_data);
    // $('#comment_list').empty();

    for (let i = 0; i < comment_data.length; i++) {
      let ID = comment_data[i]["ID"]
      let comment = comment_data[i]["comment"]

      let temp_html = `<div id="comment-item" style="margin: 40px 0">
                        <article class="media">
                          <figure class="media-left" style="margin: 1rem 2rem">
                            <p class="image is-64x64">
                              <i class="fas fa-user" style="font-size: 48px"></i>
                            </p>
                          </figure>
                          <div class="media-content" id="review">
                            <div class="content">
                              <p>
                                <strong>${ID}</strong>
                                <br />
                                ${comment}
                              </p>
                            </div>
                          </div>
                          <div class="media-right">
                            <button class="delete"></button>
                          </div>
                        </article>
                      </div>`;

      $("#com-table").append(temp_html);
    }
  },
});

// let ID = sessionStorage.getItem("username")
let ID = session["username"]
function add_comment() {
  // console.log("button clicked");
  let comment = $('#new-post').val()
  $.ajax({
    type: "POST",
    url: "/comments/update",
    data: {title_give: title, ID_give: ID, comment_give: comment},
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    }
  })
}
