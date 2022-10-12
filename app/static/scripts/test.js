var name = document.getElementById("zap").getAttribute("data-test");

new Vue({
  el: '#this-block',
  delimiters: ['[[', ']]'],
  data() {
    return {
      output: "Hello World from Vue!! " + name
    }
  },
  methods: {
    doTest() {
      this.output = 'ayah!!'
    }
  }
})


/*
<!--
{% block scripts %}
<script id="zap" src="{{url_for('static', filename='scripts/test.js')}}" data-test="123hello999"></script>
{% endblock %}
-->
*/