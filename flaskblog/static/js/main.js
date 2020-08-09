var ExcelToJSON = function () {
    
  /*this.parseExcel = function (file) {
    var reader = new FileReader();

    reader.onload = function (e) {
      var data = e.target.result;
      var workbook = XLSX.read(data, {
        type: "binary",
      });
      workbook.SheetNames.forEach(function (sheetName) {
        // Here is your object
        var XL_row_object = XLSX.utils.sheet_to_row_object_array(
          workbook.Sheets[sheetName]
        );
        console.log(XL_row_object);
        var json_object = JSON.stringify(XL_row_object);
        //console.log(JSON.parse(json_object));
        fetch("http://localhost:5000/data", {
          method: "POST",
          body: json_object,
        });
      });
    };
    reader.onerror = function (ex) {
      console.log(ex);
    };
    reader.readAsBinaryString(file);
    */
   mySpreadsheet = jexcel(document.getElementById('spreadsheet1'), {
    csv:'/jexcel/arts.csv',
    csvHeaders:true,
    tableOverflow:true,
    columns: [
        { type:'text', width:300 },
        { type:'text', width:80 },
        { type:'dropdown', width:120, source:['England','Wales','Northern Ireland','Scotland'] },
        { type:'text', width:120 },
        { type:'text', width:120 },
     ]
    });
  };
  
};

function handleFileSelect(evt) {
  var files = evt.target.files; // FileList object
  var xl2json = new ExcelToJSON();
  xl2json.parseExcel(files[0]);
}

upload = document.getElementById("upload");
console.log(upload);
upload.addEventListener("change", handleFileSelect, false);
/*var ep = new ExcelPlus();
var rows = [
  ["name1", 2, 3],
  ["name2", 4, 5],
  ["name3", 6, 7],
  ["name4", 8, 9],
  ["name5", 10, 11],
];
$(document).ready(function () {
  console.log("ready");
  $("#download").click(function () {
    console.log("clicked");
    ep.createFile("Book1").write({ content: rows }).saveAs("demo.xlsx");
  });
});*/
function ExcelGenerator(headers) {
  var excel = $JExcel.new("Calibri light 10 #111111");
  excel.set({ sheet: 0, value: "This is Sheet 0" });
  var formatHeader = excel.addStyle({
    border: "thin #111111,thin #111111,thin #111111,thin #111111",
    font: "Calibri 16  B",
  });
  var generalHeader = excel.addStyle({
    border: "thin #111111,thin #111111,thin #111111,thin #111111",
    font: "Calibri 12",
    align: "center",
  });
  for (let i = 0; i < headers.length; i++) {
    excel.set(0, i, 0, headers[i], formatHeader);
    excel.set(0, i, undefined, "auto", generalHeader);
  }
  return excel;
}
var headers = [
  "N°",
  "Libelle",
  "Unite",
  "QTE",
  "Prix Unitaire",
  "Prix Total",
  "Mois Début",
  "Mois Fin",
];
//excel.generate("SampleData.xlsx");
$(document).ready(function () {
  console.log("ready");
  $("#bor").click(function () {
    console.log("clicked");
    ExcelGenerator(headers).generate("SampleData.xlsx");
  });
  $("#planning").click(function () {
    console.log("working too");
  });
});
