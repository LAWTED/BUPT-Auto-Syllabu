<template>
  <div class="font-sans">
    <div class="relative min-h-screen flex flex-col justify-center items-center bg-gray-100 p-8">
      <div class="relative sm:max-w-sm w-full">
        <div class="card bg-blue-400 shadow-lg  w-full h-full rounded-3xl absolute  transform -rotate-6"></div>
        <div class="card bg-red-400 shadow-lg  w-full h-full rounded-3xl absolute  transform rotate-6"></div>
        <div class="relative w-full rounded-3xl  px-6 py-4 bg-gray-100 shadow-md">
          <label for="" class="block mt-3 text-xl text-gray-700 text-center font-semibold">
            北邮课表转苹果原生日历
          </label>
          <div class="mt-10">
            <div>
              <input type="id" v-model="id" placeholder="请输入学号" class="p-4 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">
            </div>

            <div class="mt-7">
              <input type="password" v-model="pw" placeholder="请输入新教务密码" class="p-4 mt-1 block w-full border-none bg-gray-100 h-11 rounded-xl shadow-lg hover:bg-blue-100 focus:bg-blue-100 focus:ring-0">
            </div>

            <div class="mt-7 flex">
            </div>

            <div class="mt-7">
              <button @click="send" class="bg-blue-500 w-full py-3 rounded-xl text-white shadow-xl hover:shadow-inner focus:outline-none transition duration-500 ease-in-out  transform hover:-translate-x hover:scale-105">
                Login
              </button>
            </div>

            <div class="flex mt-7 items-center text-center">
              <hr class="border-gray-300 border-1 w-full rounded-md">
              <label class="block font-medium text-sm text-gray-600 w-full">
                BY LAWTED
              </label>
              <hr class="border-gray-300 border-1 w-full rounded-md">
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const id = ref("");
const pw = ref("");
const send = () => {
  axios.get("https://jwgl.bupt.edu.cn/jsxsd/");
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
