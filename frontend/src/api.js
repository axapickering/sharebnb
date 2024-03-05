const BASE_URL = process.env.REACT_APP_BASE_URL || "http://localhost:5000";
console.log(BASE_URL)
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
    const url = new URL(`${ BASE_URL }/${ endpoint }`);
    const headers = {
      authorization: `Bearer ${ this.token }`,
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

      if (Array.isArray(error)) {
        throw error;
      }
      else {
        console.log(error);
        throw [error];
      }

    }

    return await resp.json();
  }

  // Individual API routes

  /** Get details on a company by handle. */

  static async getListing(id) {
    let res = await this.request(`spaces/${ id }`);
    return res;
  }

  /**Get Listings by title */
  static async getListings(nameLike) {
    let res = nameLike
      ? await this.request('spaces', { nameLike })
      : await this.request('spaces');

    console.log(res);
    return res.spaces;
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
    console.log("user data : ", userData);
    let res = await this.request('login', userData, "POST");
    return res;
  }

  /**Takes username and calls API to get the rest of the user data */
  static async getUserInfo(username) {
    let res = await this.request(`users/${ username }`);
    return res;
  }

  /** Takes in userData and calls API to update user's data with new values*/
  static async update({ username, firstName, lastName, email }) {
    let res = await this.request(`users/${ username }`,
      { firstName, lastName, email },
      "PATCH");
    return res;
  }

  /** Create new listing */
  static async uploadListing(data) {
    console.log(data);
    const formDataObj = new FormData();
    formDataObj.append("title", data.title);
    formDataObj.append("description", data.description);
    formDataObj.append("price", data.price);
    formDataObj.append("address", data.address);
    formDataObj.append("image", data.image);
    console.log("DATA OBJ", formDataObj);
    console.log(this.token);
    const response = await fetch(`${ BASE_URL }/spaces`, {
      method: 'POST',
      body: formDataObj,
      headers: {
        "Authorization": `Bearer ${ this.token }`,
      }
    });

    return response;
  }

  static async deleteListing(id) {
    console.log("id : ", id);
    let res = await this.request(`spaces/${ id }`, undefined, "DELETE");
    return res;
  }

  /** BOOKINGS */

  /**Get a booking */
  static async getBooking(id) {
    const res = await this.request(`bookings/${ id }`);
    return res;
  }

  /**Get all bookings */
  static async getBookings(title) {
    let res = title
      ? await this.request('bookings', { title })
      : await this.request(`bookings`);
    return res.bookings;
  }

  static async createBooking(bookingData) {
    let res = await this.request('bookings', bookingData, "POST");
    return res;
  }
}

export default ShareBnbApi;
