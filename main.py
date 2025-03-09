import streamlit as st
import re
import random
import string

# List of common weak passwords to blacklist
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "password123"]

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Reset warnings
    st.session_state.warnings = []

    # Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        st.error("❌ Password is too common and easily guessable.")
        return 0

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9)")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*)")

    # Store feedback in session state
    st.session_state.warnings = feedback
    return score

def generate_strong_password(length=12):
    """Generate a strong password with a mix of characters"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    st.set_page_config(page_title="Password Strength Checker", page_icon="🔒")
    
    st.title("🔒 Password Strength Checker")
    st.markdown("Check your password strength and get improvement suggestions!")

    # Password input column
    col1, col2 = st.columns([3, 1])
    with col1:
        password = st.text_input("Enter your password:", type="password", 
                                placeholder="Type or generate a password...")
    
    # Generate password button
    with col2:
        if st.button("Generate Strong Password"):
            generated_pw = generate_strong_password()
            st.session_state.generated_password = generated_pw

    # Display generated password
    if 'generated_password' in st.session_state:
        st.markdown(f"**Generated Password:** `{st.session_state.generated_password}`")
        if st.button("📋 Copy to Clipboard"):
            st.session_state.password = st.session_state.generated_password

    # Check password button
    if st.button("Check Strength", type="primary"):
        if password:
            score = check_password_strength(password)
            
            # Display strength indicator
            with st.container():
                st.subheader("Strength Assessment")
                
                if score == 4:
                    st.success("✅ Strong Password!")
                    st.balloons()
                elif score == 3:
                    st.warning("⚠️ Moderate Password")
                else:
                    st.error("❌ Weak Password")

                # Show feedback messages
                if st.session_state.warnings:
                    st.markdown("**Improvement Suggestions:**")
                    for warning in st.session_state.warnings:
                        st.markdown(f"- {warning}")
        else:
            st.warning("Please enter a password first!")

    # Add footer
    st.markdown("---")
    st.markdown("*Made with ❤️ By Atiq Sarwar*")

if __name__ == "__main__":
    main()