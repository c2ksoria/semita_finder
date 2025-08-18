# 🥖 Semita Finder

Semita Finder is a **web platform** that connects local businesses with nearby customers.
It allows users to discover businesses around them, place orders, and track their status, while businesses can manage their products and received orders.

## 🌱 Project Origin

Semita Finder was born in ***San Juan, Argentina***, with the goal of making it easier to find and buy "semitas", a traditional local baked good deeply rooted in the region’s culture.

In San Juan, semitas are sold in bakeries and small family-run businesses, but customers often don’t know which nearby shops have them available or when those shops are open. This project started as a solution to that local problem, by:

Allowing users to locate nearby bakeries or shops that sell semitas.

Making it possible to browse semita varieties (e.g., semitón, semita con chicharrones, raspadita) and place an order in advance.

Helping businesses increase visibility and better manage their incoming orders.

At this stage, the system is not intended for other types of products. Its core focus is the commercialization and discovery of semitas and their traditional variants.

## 🚀 Project Overview

* Built as a ***full-stack application*** with ***Django REST Framework*** (backend) and ***Vue.js*** (frontend).

* Core idea: ***proximity-based search*** – users see businesses close to their location and interact directly.

* Supports ***order creation, order tracking, and business order management.***

* Supports ***products creation and management.***

* Designed as an MVP to be extended with additional features.

## ✨ Key Features
### 🔎 Proximity Search

* Uses the ***current user location*** to find nearby businesses.

* Businesses within a configurable ***search radius*** are displayed.

* Results appear in:

* ***Interactive map markers.***

* ***Table view*** with business information.

### 📏 Search Radius Configuration

* Users can adjust the ***search radius*** dynamically.

* Wider radius → more businesses listed.

## 🏪 Business Display

### Each business is shown on:

* The map as a clickable marker.

* The results table, including:
    - Business name.
    - Address.
    - Opening status:
        - Open now
        - Closed
        - Opening soon (calculated dynamically from current system time vs. schedule).

## 🛒 Ordering Flow

* Each commerce listed in the search results table (alongside the map) includes a "Buy" button.

* Clicking this button takes the user to the order creation screen, where they can:

    * Choose a date and time for pickup.

    * Browse all available products from that commerce.

    * Select desired quantities for each product.

* The system validates that orders cannot be created with zero quantities.

## 🛒 Orders – Client Perspective

* Clients can:

    * Browse products of a business.

    * Create new orders.

    * View their own orders list with details:

        ```ID | Business | Pickup date & time | Total | Status | Actions```
    * Open a ***detailed order view.***

## 📦 Order Detail

* Shows:

    * Items with quantity, subtotal, and total.

    * ***Order history (status timeline)*** with timestamps.

## 🏬 Orders – Business Perspective (Received Orders)

* Businesses access a list of all ***orders received.***

* Includes:

    * Same summary info as client orders.

    * Full order detail (items, totals, comments).

    * ***Order history.***

    * Ability to ***update order status*** (e.g., “Registered → In preparation → Ready → Delivered”).

    * Once an order is marked ***Delivered***, it becomes ***read-only*** (no further edits).

## 🏪 Commerce Details

* Users can also access a Commerce Detail Page, which displays:

    * The name, description, and address of the shop.
    * The opening hours, including multiple time ranges per day.
    * Uploaded photos of the commerce.
    * A full list of products offered by the commerce, with photos when available.

## 🛠️ Tech Stack

* Backend: Django + Django REST Framework
* Frontend: Vue.js (Composition API)
* Database: PostgreSQL
* API Documentation: Swagger (drf-yasg)
* Authentication: JWT
* Deployment: Docker (planned)

## 📡 API Highlights

* Businesses

    * ```GET /comercios/cercanos/``` → Businesses near user location (with radius).

    * ```GET /comercio/:id/``` → Business detail (products, images, schedules).

* Orders

    * ```POST /pedido/``` → Create new order.

    * ```GET /pedido/mis-pedidos/``` → Client’s orders.

    * ```GET /pedido/mis-pedidos/:id/``` → Client order detail.

    * ```GET /pedido/pedidos-recibidos/``` → Business received orders.

    * ```GET /pedido/pedidos-recibidos/:id/``` → Business order detail.
    * ```POST /pedido/:id/cambiar-estado/``` → Change order status (restricted by business).

## 🛤️ Roadmap (Next Features)

* 🖼️ Product images integration.

* ⏰ Unified date & time picker for order pickup.

* 📏 Improved distance calculation (approximate kilometers).

* 🔔 Highlight row in results table when clicking a business marker.

* 🎛️ More flexible schedule editing (multiple time slots per day).

* 🚫 Backend-level restriction on delivered order editing.

* 🌍 Multi-language documentation (README + Wiki in EN/ES).

## 📖 Credits

Developed by Carlos Valdemar Soria with guidance from GPT-5 (OpenAI).