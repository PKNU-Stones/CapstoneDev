<template>
  <div class="card-body">
    <table v-for ="i in 2" :key="i" class="inputTable">
      <thead>
        <tr>
          <td class="td-custom" v-for="j in 6" :key="j">{{FEATURE_names[j + 6*i - 7]}}</td>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-for="j in 6" :key="j">
            <input
              :value="FEATURE_values[j + 6*i - 7]"
              type="text"
              class="history-feature-value-box"
              readonly
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  methods: {},
  props: {
    FEATURE_values: Array
  },
  data() {
    return {
      FEATURE_names: [
        "코일의 평균 입측 두께",
        "upper 롤 이동값",
        "lower 롤 이동값",
        "밴딩 DS",
        "LH tension",
        "RH tension",
        "POR tension",
        "POR tension (N/mm²)",
        "롤 힘",
        "롤 속도",
        "좌 냉각수 유량",
        "우 냉각수 유량"
      ]
    };
  },
  components: {}
};
</script>
