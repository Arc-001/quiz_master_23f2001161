In JavaScript, `call()`, `apply()`, and `bind()` are methods that allow you to manipulate the `this` context of a function. This essentially means they let you control what `this` refers to when a function is executed. Here's a breakdown of each:

**1. call()**

* The `call()` method invokes a function directly, and it allows you to specify the `this` value.
* Arguments are passed to the function individually.

    * Example:
        ```javascript
        function greet(name) {
          console.log(`Hello, ${name}! My name is ${this.name}.`);
        }
        let person = { name: "John" };
        greet.call(person, "Alice"); // Output: Hello, Alice! My name is John.
        ```

**2. apply()**

* The `apply()` method is very similar to `call()`, but it takes arguments as an array.
* It also invokes the function immediately.

    * Example:
        ```javascript
        function greet(name, lastname) {
            console.log("hello "+ name + " "+ lastname + " my name is " + this.name);
        }
        let person = {name: "John"};
        greet.apply(person, ["Alice","Smith"]);
        ```

**3. bind()**

* The `bind()` method creates a new function with the specified `this` value.
* It does not invoke the function immediately. Instead, it returns a new function that can be called later.
* It can also have preset arguments.

    * Example:
        ```javascript
        function greet() {
          console.log(`Hello, my name is ${this.name}.`);
        }
        let person = { name: "John" };
        let greetPerson = greet.bind(person);
        greetPerson(); // Output: Hello, my name is John.
        ```

**Key Differences Summarized:**

* **Invocation:**
    * `call()` and `apply()` invoke the function immediately.
    * `bind()` returns a new function that must be invoked separately.
* **Arguments:**
    * `call()` takes arguments individually.
    * `apply()` takes arguments as an array.
    * `bind()` can take arguments individually, and those arguments will be permanently set into the new function that is returned.

Prototype chaining is a fundamental concept in JavaScript that allows objects to inherit properties and methods from other objects. It's the mechanism behind prototypal inheritance, which is different from classical inheritance found in languages like Java or C++.

Here's a breakdown with examples:

**Understanding Prototypes**

* **Every object in JavaScript has a prototype.** This prototype is itself an object.
* **When you try to access a property or method of an object, JavaScript first looks for it in the object itself.** If it's not found, it looks in the object's prototype. If it's still not found, it looks in the prototype's prototype, and so on, until it reaches the end of the prototype chain (which is typically `null`).
* **The `__proto__` property (or `Object.getPrototypeOf()` method) is used to access an object's prototype.** While `__proto__` exists, it is recommended to use `Object.getPrototypeOf()` and `Object.setPrototypeOf()` where possible, for better compatibility.
* **Functions also have a `prototype` property.** When a function is used as a constructor (with the `new` keyword), the `prototype` property of the function is used to set the `__proto__` of the newly created object.

**Example 1: Basic Prototype Chain**

```javascript
// Constructor function
function Animal(name) {
  this.name = name;
}

// Add a method to the Animal prototype
Animal.prototype.sayName = function() {
  console.log("My name is " + this.name);
};

// Create an instance of Animal
const dog = new Animal("Buddy");

// Access the method
dog.sayName(); // Output: My name is Buddy

// Check the prototype chain
console.log(Object.getPrototypeOf(dog) === Animal.prototype); // true
console.log(Object.getPrototypeOf(Animal.prototype) === Object.prototype); // true
console.log(Object.getPrototypeOf(Object.prototype)); // null
```

**Explanation:**

1.  We define a constructor function `Animal`.
2.  We add a `sayName` method to `Animal.prototype`.
3.  We create an instance of `Animal` called `dog`.
4.  When we call `dog.sayName()`, JavaScript first looks for `sayName` in the `dog` object itself. Since it's not found, it looks in `dog.__proto__` (which is `Animal.prototype`). The method is found there, and it's executed.
5.  The `Object.getPrototypeOf()` calls demonstrate the chain: `dog`'s prototype is `Animal.prototype`, `Animal.prototype`'s prototype is `Object.prototype`, and `Object.prototype`'s prototype is `null`.

**Example 2: Inheriting from Another Prototype**

```javascript
function Animal(name) {
  this.name = name;
}

Animal.prototype.sayName = function() {
  console.log("My name is " + this.name);
};

function Dog(name, breed) {
  Animal.call(this, name); // Call the Animal constructor
  this.breed = breed;
}

// Set Dog's prototype to Animal's prototype
Dog.prototype = Object.create(Animal.prototype);

// Add a method specific to Dog
Dog.prototype.bark = function() {
  console.log("Woof!");
};

// Create a Dog instance
const myDog = new Dog("Max", "Golden Retriever");

myDog.sayName(); // Output: My name is Max
myDog.bark(); // Output: Woof!

console.log(Object.getPrototypeOf(myDog) === Dog.prototype); //true
console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype); //true
```

**Explanation:**

1.  We define `Animal` as before.
2.  We define `Dog`, which "inherits" from `Animal`.
3.  `Animal.call(this, name)` calls the `Animal` constructor with the `Dog` instance as `this`, ensuring the `name` property is set.
4.  `Dog.prototype = Object.create(Animal.prototype)` sets `Dog`'s prototype to a new object whose prototype is `Animal.prototype`. This establishes the inheritance.
5.  We add a `bark` method to `Dog.prototype`.
6.  `myDog` can now access both `sayName` (from `Animal.prototype`) and `bark` (from `Dog.prototype`).

**Key Points**

* Prototype chaining is the core of JavaScript's inheritance model.
* It allows for code reuse and efficient memory usage.
* Understanding prototype chains is crucial for writing effective JavaScript code.
* `Object.create()` is the preferred way to create a new object and set its prototype.
* Avoid direct manipulation of `__proto__` when possible.

