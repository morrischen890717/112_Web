returnDateTime = function () {
  const currentDateTime = new Date();
  const year = currentDateTime.getFullYear();
  const month = ("0" + (currentDateTime.getMonth() + 1)).slice(-2);
  const day = ("0" + currentDateTime.getDate()).slice(-2);
  const hours = ("0" + currentDateTime.getHours()).slice(-2);
  const minutes = ("0" + currentDateTime.getMinutes()).slice(-2);
  const seconds = ("0" + currentDateTime.getSeconds()).slice(-2);

  const currentDateTimeString =
    year +
    "/" +
    month +
    "/" +
    day +
    " " +
    hours +
    ":" +
    minutes +
    ":" +
    seconds;
  return currentDateTimeString;
};

addHistory = function (num) {
  const history_table = document.getElementById("history-table");

  tr = document.createElement("tr");

  td_time = document.createElement("td");
  td_device = document.createElement("td");

  td_time.innerHTML = returnDateTime();
  td_device.innerHTML = num;

  tr.appendChild(td_time);
  tr.appendChild(td_device);

  history_table.appendChild(tr);
};

apply = function (num) {
  console.log("aaa");
  addHistory(num);
  console.log("bbb");
  showToast("Apply Successfully", "success", 5000);
  console.log("ccc");
};
