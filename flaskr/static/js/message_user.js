var messageBody = document.querySelector("#msgBody");
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

$(document).ready(function () {
  $("#send").click(function () {
    $.ajax({
      url: "controller/insertChat.php",
      method: "POST",
      data: {
        toID: "<?=$_GET['toID']?>",
        message: $("#message").val(),
      },
      dataType: "text",
      success: function (data) {
        $("#message").val("");
      },
    });
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
  });

  setInterval(function () {
    $.ajax({
      url: "controller/realtimeChat.php",
      method: "POST",
      data: {
        toID: "<?=$_GET['toID']?>",
      },
      dataType: "text",
      success: function (data) {
        $("#msgBody").html(data);
      },
    });
  }, 700);
});
