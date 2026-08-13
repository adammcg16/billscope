<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NBN Plan Selector & Form</title>
    <style>
        :root {
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --input-bg: #f4f6f8;        /* Lighter, eye-friendly color */
            --input-border: #cbd5e1;    /* Gentle gray border */
            --input-focus: #3b82f6;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background-color: var(--card-bg);
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            width: 100%;
            max-width: 480px;
        }

        h2 {
            margin-top: 0;
            margin-bottom: 24px;
            font-size: 24px;
            font-weight: 600;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 14px;
        }

        /* Updated input styling: lighter background, softer borders, comfortable contrast */
        input[type="text"],
        input[type="email"],
        select {
            width: 100%;
            padding: 12px 16px;
            background-color: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 8px;
            color: var(--text-main);
            font-size: 15px;
            box-sizing: border-box;
            transition: all 0.2s ease;
        }

        input[type="text"]:focus,
        input[type="email"]:focus,
        select:focus {
            outline: none;
            background-color: #ffffff;
            border-color: var(--input-focus);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }

        select option {
            background-color: #ffffff;
            color: var(--text-main);
        }

        button {
            width: 100%;
            padding: 12px 16px;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease;
            margin-top: 8px;
        }

        button:hover {
            background-color: var(--primary-hover);
        }
    </style>
</head>
<body>

    <div class="container">
        <h2>Select Your nbn® Plan</h2>
        <form>
            <div class="form-group">
                <label for="fullName">Full Name</label>
                <input type="text" id="fullName" placeholder="Enter your full name">
            </div>

            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" placeholder="Enter your email">
            </div>

            <div class="form-group">
                <label for="nbnSpeed">Choose nbn® Speed Tier</label>
                <select id="nbnSpeed">
                    <option value="" disabled selected>Select a speed tier</option>
                    <option value="nbn25">nbn® 25 (Home Basic II)</option>
                    <option value="nbn50">nbn® 50 (Home Standard)</option>
                    <option value="nbn100">nbn® 100 (Home Fast)</option>
                    <option value="nbn250">nbn® 250 (Home Superfast)</option>
                    <option value="nbn1000">nbn® 1000 (Home Ultrafast)</option>
                </select>
            </div>

            <button type="submit">Check Availability</button>
        </form>
    </div>

</body>
</html>
