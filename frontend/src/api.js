const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:5000";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class ShareBnbApi {
  // Remember, the backend needs to be authorized with a token
  // We're providing a token you can use to interact with the backend API
  // DON'T MODIFY THIS TOKEN

  static token = "";

  static async request(endpoint, data = {}, method = "GET") {
    const url = new URL(`${BASE_URL}/${endpoint}`);
    const headers = {
      authorization: `Bearer ${this.token}`,
      'content-type': 'application/json',
    };

    url.search = (method === "GET")
      ? new URLSearchParams(data).toString()
      : "";

    // set to undefined since the body property cannot exist on a GET method
    const body = (method !== "GET")
      ? JSON.stringify(data)
      : undefined;

    const resp = await fetch(url, { method, body, headers });

    //fetch API does not throw an error, have to dig into the resp for msgs
    if (!resp.ok) {
      console.error("API Error:", resp.statusText, resp.status);
      const { error } = await resp.json();

      if (Array.isArray(error.message)) {
        throw error.message;
      }
      else {
        console.log(error.message);
        throw [error.message];
      }

    }

    return await resp.json();
  }

  // Individual API routes

  /** Get details on a company by handle. */

  static async getListing(id) {
    let res = await this.request(`spaces/${id}`);
    return res;
  }

  /**Get Listings by title */
  static async getListings(nameLike) {
    let res = nameLike
      ? await this.request('spaces', { nameLike })
      : await this.request('spaces');

    return res.companies;
  }

  /**Get all jobs */
  static async getBooking(title) {
    let res = title
      ? await this.request('jobs', { title })
      : await this.request(`jobs`);
    return res.jobs;
  }

  // User API routes

  /**Takes user data from signup form calls api to register the user, returns
   * response
   */
  static async signup(userData) {
    let res = await this.request('signup', userData, "POST");
    return res;
  }

  /**Takes username and password from login form and signs in the user via APi call */
  static async login(userData) {
    console.log("user data : ",userData)
    let res = await this.request('login', userData, "POST");
    return res;
  }

  /**Takes username and calls API to get the rest of the user data */
  static async getUserInfo(username) {
    let res = await this.request(`users/${username}`);
    return res;
  }

  /** Takes in userdata and calls API to update user's data with new values*/
  static async update({ username, firstName, lastName, email }) {
    let res = await this.request(`users/${username}`,
      { firstName, lastName, email },
      "PATCH");
    return res;
  }

}

export default ShareBnbApi;
