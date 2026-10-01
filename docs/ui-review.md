# UI review and presentation guide

## Implemented

- Consistent Submit file → Inspect file → Prediction stages and a direct overview action.
- Research-focused copy without repository paths or integration jargon; the requested IoT Research Lab sidebar branding is retained.
- Session-only upload retention across navigation, explicit replacement/cancellation and clearing.
- A 280-pixel text preview with wrapped lines, an 8 KiB inspection limit, and a visible truncation notice.
- Distinct no-file, empty-file, whitespace-preview, unreadable-preview, and unavailable-prediction states.
- Semantic page titles and section headings, visible widget labels, and native focus styling.
- Native wrapping columns and filename wrapping; a supported 1120-pixel maximum content container and 260-pixel initial sidebar width.
- Compact overview cards and headers, aligned input/inspection and prediction/results panels, and paired research objective/approach cards.

Inference contracts and unavailable inference behavior are unchanged. No research results, model outputs, feature definitions, or preprocessing were added.

## Verification status

Automated interaction checks cover navigation, upload persistence, replacement (including the same filename), cancellation, clearing, separate-session isolation, long previews, and disabled prediction. These tests do not establish rendered accessibility or responsiveness.

Presentation-polish verification: all 16 existing tests passed without test changes. Dependency consistency, imports, and Python compilation passed. A fresh Streamlit process passed its startup health check. Theme colors remain unchanged; the footer now inherits the native text color. Prior calculated contrast for the retained body and teal colors against both configured backgrounds ranges from 4.87:1 to 13.79:1. This calculation does not verify native widget colors or browser-rendered states.

The user visually approved the existing design before this pass. No browser connection was available to verify the latest polish. New screenshots have therefore not been captured. The following checks remain pending:

| Check | Acceptance criteria |
| --- | --- |
| Desktop: 1440×900, 1366×768, and 1280×720 | All three pages are readable; card spacing is consistent; prediction status is easy to locate. |
| Narrow screen: 390×844 | Cards stack in workflow order; navigation remains accessible; no page-level horizontal overflow. |
| Browser zoom: 200% | Labels, controls, and long filenames remain readable without overlapping or clipped content. |
| Keyboard | Tab/Shift+Tab can reach navigation and upload controls; radio navigation and action buttons work; focus remains visible. |
| Screen reader | Page title, section headings, file selection, warnings, and unavailable prediction are announced meaningfully. |
| Contrast | Check rendered text, disabled controls, focus rings, and native alerts in the configured light theme. |
| Long content | Long filenames wrap; many preview lines stay in the bounded scroll region; the full file is not implied to have been inspected. |

DOM-dependent CSS has been removed. Layout uses documented container widths/gaps, wrapping columns, and wrapping text. CSS styles only application-owned eyebrow/footer classes and reads the accent from the theme. Native navigation, focus indicators, and sidebar collapse controls remain available. Recheck wrapping and keyboard behavior visually after upgrades.

## Supported presentation configuration

`.streamlit/config.toml` sets `client.toolbarMode = "viewer"` to hide developer options while retaining normal viewer controls. It does not remove all Streamlit chrome. Heading sizes use `theme.headingFontSizes`, preserving the existing main typography hierarchy without global heading CSS. The theme stays light with the existing teal accent.

See the official [configuration reference](https://docs.streamlit.io/develop/api-reference/configuration/config.toml), [page configuration](https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config), and [container API](https://docs.streamlit.io/develop/api-reference/layout/st.container).

Restart the local server to ensure all configuration changes are applied. For normal developer toolbar controls, use this non-persistent override:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --client.toolbarMode developer
```

After browser verification, save screenshots in `docs/screenshots/`: overview, empty submission, readable preview, unavailable preview, research notes, and a narrow-screen submission view. Use only approved, non-sensitive inspection text and do not label it as model-ready data.

## Eight-minute presentation

| Time | Presenter focus |
| --- | --- |
| 0:00–1:30 | Overview: research problem and project objective. |
| 1:30–3:00 | Research notes: stated learning approach and strict LOAFO evaluation plan. |
| 3:00–5:30 | Data submission: choose an approved local file, inspect details, and show retention across navigation. |
| 5:30–6:30 | Prediction area: explain that the actual model is still being trained separately. |
| 6:30–8:00 | Recap the implemented UI and the planned model integration. |

Rehearse with the presentation display. Use Clear file before starting a new demonstration. Do not present inspected content as a validated model input or claim model accuracy from this interface.
