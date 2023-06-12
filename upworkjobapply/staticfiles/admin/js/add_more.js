document.addEventListener("DOMContentLoaded", function () {
  var input_plan_feat = document.getElementById("id_plan_features");

  var saveBtn = document.createElement("button");
  saveBtn.type = "button";
  saveBtn.classList.add("btn", "btn-info", "save-btn");
  saveBtn.textContent = "Save Features";

  var plan_feat_parent = input_plan_feat.parentElement;
  var addBtn = document.createElement("button");
  addBtn.textContent = "Add More Feature";
  addBtn.type = "button";
  addBtn.classList.add("addBtn", "btn", "btn-primary");

  var clrBtn = document.createElement("button");
  clrBtn.textContent = "Clear All";
  clrBtn.type = "button";
  clrBtn.classList.add("clrBtn", "btn", "btn-primary");

  plan_feat_parent.parentElement.insertAdjacentElement("afterend", clrBtn);
  plan_feat_parent.parentElement.insertAdjacentElement("afterend", saveBtn);
  plan_feat_parent.parentElement.insertAdjacentElement("afterend", addBtn);

  var plan_feat_parent_parent = plan_feat_parent.parentElement;

  if (input_plan_feat && input_plan_feat.value) {
    try {
      var f_input_p_v = JSON.parse(input_plan_feat.value);
      const all_val_ready = f_input_p_v.slice(1);
      all_val_ready.forEach((fe) => {
        plan_feat_parent_parent.insertAdjacentElement(
          "afterend",
          addBtnFunc(fe)
        );
      });
    } catch (err) {
      ("");
    }
  }

  document.addEventListener("click", function (e) {
    if (e.target) {
      if (e.target.classList.contains("addBtn")) {
        const n_ele = addBtnFunc();

        plan_feat_parent_parent.insertAdjacentElement("afterend", n_ele);
      }

      if (e.target.classList.contains("save-btn")) {
        var mainInputElement = document.querySelector("#id_plan_features");
        var addiInputElement = document.querySelectorAll(
          'input[name="added_plan_features"]'
        );

        var allValuesTemp1 = [];

        if (mainInputElement && mainInputElement.value) {
          var mainInputElement_val = JSON.parse(mainInputElement.value);

          mainInputElement_val.forEach((avt) => {
            allValuesTemp1.push(`"${avt}"`);
          });

          mainInputElement.value = "";
        }

        var allValuesTemp2 = [];

        for (let i = 0; i < addiInputElement.length; i++) {
          const elementPlan = addiInputElement[i];

          if (elementPlan.value) {
            allValuesTemp2.push(`"${elementPlan.value}"`);
          }
        }

        var totalVal = [...allValuesTemp1, ...allValuesTemp2];

        // console.log(totalVal);

        mainInputElement.value = `[${totalVal}]`;
      }

      if (e.target.classList.contains("rm_btn")) {
        var crrRmVal = e.target.parentNode.querySelector(
          "#added_id_plan_features"
        ).value;
        e.target.parentNode.remove();

        try {
          var id_plan_features_re = document.querySelector("#id_plan_features");
          var id_plan_features_re_val = JSON.parse(id_plan_features_re.value);

          id_plan_features_re_val.splice(
            id_plan_features_re_val.indexOf(crrRmVal),
            1
          );

          var tempPlanVal3 = [];

          id_plan_features_re_val.forEach((el3) => {
            tempPlanVal3.push(`"${el3}"`);
          });

          id_plan_features_re.value = `[${tempPlanVal3}]`;
          // console.log(id_plan_features_re_val);
          // console.log(tempPlanVal3);
        } catch (err) {
          ("");
        }

        // mainInputElement.splice(mainInputElement.indexof(crrRmVal));

        // start from here
      }
      if (e.target.classList.contains("clrBtn")) {
        document.querySelector("#id_plan_features").value = "";

        document.querySelectorAll("#added_id_plan_features").forEach((ADP) => {
          ADP.value = "";
        });
      }
    }
  });

  function addBtnFunc(val = null) {
    var new_element = plan_feat_parent.cloneNode(true);

    new_element.classList.add("form-row", "field-plan_features");
    var selLabel = new_element.querySelector("label");
    new_element.removeChild(selLabel);

    var rm_Btn = document.createElement("button");
    rm_Btn.classList.add("rm_btn", "btn", "btn-warning");
    rm_Btn.type = "button";
    rm_Btn.textContent = "Remove";

    new_element.appendChild(rm_Btn);

    var selinput = new_element.querySelector("input");
    selinput.value = "";
    selinput.name = "added_plan_features";
    selinput.id = "added_id_plan_features";

    if (val) {
      selinput.value = val;
    }

    new_element.querySelector(".help").remove();

    return new_element;
  }

  // var rmContBtn = document.querySelectorAll(".rm_btn");
  // if (rmContBtn) {
  //   rmContBtn.forEach((CB) => {
  //     CB.addEventListener("click", (e) => {
  //       console.log(e);
  //     });
  //   });
  // }
});
