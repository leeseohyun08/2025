st.markdown(
    f"""
    <style>
      :root {{
        --primary: {primary};
        --secondary: {secondary};
        --accent: {accent};
        --text: {text_color};
        --panel: {panel_bg};
        --card: {card_bg};
        --border: {border_color};
      }}
      .app-root {{
        background: {bg_gradient};
        height: 10vh;  /* ✅ 이 줄만 바꿔줌 (기존 min-height: 100vh 제거) */
      }}
      .glass {{
        background: var(--panel);
        backdrop-filter: blur(10px);
        border: 1px solid {primary}33;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px #00000022;
      }}
      ...
    </style>
    <div class="app-root"></div>
    """,
    unsafe_allow_html=True
)
