
  <div class="box">
    <p>{{ OMIR.name }} : {{ OMIR.rtgs }} </p>
  </div>

  <div class="box">
    {%  for i in interbank.items %}
    <p>{{ interbank.name }} : {{ interbank.rtgs }}  </p>
    {% endfor %}
  </div>

  <div class="box">
    <p>{{ zimrates_bond.name }} : {{ zimrates_bond.rtgs }}  </p>
  </div>

  <div class="box">
    <p>{{ bluemari_info.name }} : {{bluemari_info.rtgs }}  </p>
  </div>
